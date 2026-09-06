param(
    [string]$BaseUrl = 'http://127.0.0.1:8765',
    [Parameter(Mandatory=$true)][string]$Token
)

$ErrorActionPreference = 'Stop'
$headers = @{ 'X-SIIAOS-Token' = $Token }

$health = Invoke-RestMethod -Method Get -Uri "$BaseUrl/health"
if (-not $health.ok) { throw 'Health check failed' }

$summary = Invoke-RestMethod -Method Get -Uri "$BaseUrl/registry/summary" -Headers $headers

$observation = @{
    subject_id = 'sandy:bridge-v4'
    type = 'smoke_test'
    observed_at = (Get-Date).ToString('o')
    confidence = 1.0
    method = 'powershell-smoke'
    visibility = 'local-only'
    facts = @{
        health = $health
        registry_summary = $summary
    }
} | ConvertTo-Json -Depth 8

$result = Invoke-RestMethod -Method Post -Uri "$BaseUrl/observations" -Headers $headers -ContentType 'application/json' -Body $observation

[pscustomobject]@{
    health_ok = $health.ok
    version = $health.version
    observation_accepted = $result.accepted
    observation_id = $result.id
    registry_summary = $summary
} | ConvertTo-Json -Depth 8
