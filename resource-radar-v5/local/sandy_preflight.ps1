param(
    [string[]]$SearchRoots = @('C:\GitHub','D:\GitHub','D:\GITHUB','D:\SIIAOS','C:\SIIAOS'),
    [string]$ReportDir = "$env:TEMP\siiaos-sandy-preflight"
)

$ErrorActionPreference = 'Continue'
$ts = Get-Date -Format 'yyyyMMdd-HHmmss'
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null
$report = Join-Path $ReportDir "sandy-preflight-$ts.json"

function CmdInfo([string]$Name, [string[]]$Args = @('--version')) {
    try {
        $cmd = Get-Command $Name -ErrorAction Stop
        $out = & $Name @Args 2>&1 | Out-String
        [pscustomobject]@{ found=$true; path=$cmd.Source; output=$out.Trim() }
    } catch {
        [pscustomobject]@{ found=$false; path=$null; output=$_.Exception.Message }
    }
}

$repos = @()
foreach ($root in $SearchRoots) {
    if (-not (Test-Path $root)) { continue }
    Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $gitDir = Join-Path $_.FullName '.git'
        if (Test-Path $gitDir) {
            $branch = ''
            $remote = ''
            try { $branch = git -C $_.FullName branch --show-current 2>$null }
            catch {}
            try { $remote = git -C $_.FullName remote get-url origin 2>$null }
            catch {}
            $repos += [pscustomobject]@{
                path = $_.FullName
                name = $_.Name
                branch = ($branch | Out-String).Trim()
                remote = ($remote | Out-String).Trim()
            }
        }
    }
}

$ports = @()
foreach ($p in 8765,8790,8791,1234,1235,3000,8080) {
    try {
        $hit = Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction Stop
        $ports += [pscustomobject]@{ port=$p; listening=$true; processIds=@($hit.OwningProcess | Sort-Object -Unique) }
    } catch {
        $ports += [pscustomobject]@{ port=$p; listening=$false; processIds=@() }
    }
}

$docker = CmdInfo 'docker'
$python = CmdInfo 'py' @('--version')
if (-not $python.found) { $python = CmdInfo 'python' @('--version') }
$git = CmdInfo 'git'
$wsl = CmdInfo 'wsl' @('--status')

$payload = [ordered]@{
    generated_at = (Get-Date).ToString('o')
    computer_name = $env:COMPUTERNAME
    user_name = $env:USERNAME
    search_roots = $SearchRoots
    tools = [ordered]@{
        git = $git
        python = $python
        docker = $docker
        wsl = $wsl
    }
    repositories = $repos
    listening_ports = $ports
    recommendations = @(
        'Do not move or delete any repository based on this report.',
        'Confirm the canonical local twinSIIAOS clone before starting the bridge.',
        'Confirm whether port 8765 is free before bridge startup.',
        'Treat D:\SIIAOS\radar-core as target-only until explicitly validated.'
    )
}

$payload | ConvertTo-Json -Depth 8 | Set-Content -Path $report -Encoding UTF8
Write-Host "PRELIGHT_OK"
Write-Host "REPORT=$report"
Write-Host "REPOS=$($repos.Count)"
Write-Host "PORT8765_LISTENING=$((($ports | Where-Object port -eq 8765).listening))"
