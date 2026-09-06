param(
    [Parameter(Mandatory=$true)][string]$RepoPath,
    [string]$Root = 'D:\SIIAOS\radar-core',
    [int]$Port = 8765
)

$ErrorActionPreference = 'Stop'
$bridge = Join-Path $RepoPath 'resource-radar-v5\local\siiaos_bridge_v4.py'
if (-not (Test-Path $bridge)) { throw "Bridge introuvable: $bridge" }

if (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue) {
    throw "Le port $Port est deja ecoute. Ne pas lancer un second bridge avant identification du processus."
}

if (-not (Test-Path $Root)) {
    New-Item -ItemType Directory -Force -Path $Root | Out-Null
}

$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    & py $bridge --root $Root --port $Port
} else {
    & python $bridge --root $Root --port $Port
}
