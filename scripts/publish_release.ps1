param([string]$Version = 'v1.1.0')
$ErrorActionPreference = 'Stop'
$leapworkRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $leapworkRoot
if ($Version -notmatch '^v\d+\.\d+\.\d+$') { throw 'Versão inválida.' }
$leapworkRepo = 'NotOnepiecePlease/LeapworkdKnowledgeBase'
$leapworkPortable = Join-Path $leapworkRoot '.publication\gh\bin\gh.exe'
$leapworkGh = if (Test-Path -LiteralPath $leapworkPortable) { $leapworkPortable } else { (Get-Command gh -ErrorAction Stop).Source }
if (Test-Path -LiteralPath (Join-Path $leapworkRoot '.publication\gh-config')) {
    $env:GH_CONFIG_DIR = Join-Path $leapworkRoot '.publication\gh-config'
}
function Invoke-LeapworkGh {
    & $leapworkGh @args
    if ($LASTEXITCODE -ne 0) { throw 'O comando do GitHub falhou; a publicação foi interrompida.' }
}
function Invoke-LeapworkGit {
    & git --git-dir=.publication/git --work-tree=. @args
    if ($LASTEXITCODE -ne 0) { throw 'O comando Git falhou; a publicação foi interrompida.' }
}
Invoke-LeapworkGh auth status
# Confere arquivos e hashes antes de publicar qualquer alteração.
$leapworkChecksums = Join-Path $leapworkRoot 'dist\SHA256SUMS.txt'
foreach ($leapworkLine in Get-Content -LiteralPath $leapworkChecksums) {
    $leapworkParts = $leapworkLine -split '\s+', 2
    $leapworkFile = Join-Path $leapworkRoot ('dist\' + $leapworkParts[1])
    if ((Get-FileHash -LiteralPath $leapworkFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $leapworkParts[0]) {
        throw "Checksum inválido: $leapworkFile"
    }
}
if (-not (Test-Path -LiteralPath '.publication\git\HEAD')) {
    Invoke-LeapworkGit init -b main
    Invoke-LeapworkGit remote add origin "https://github.com/$leapworkRepo.git"
}
Invoke-LeapworkGit config http.sslBackend openssl
$leapworkHelper = '!"' + ($leapworkGh -replace '\\', '/') + '" auth git-credential'
Invoke-LeapworkGit config credential.helper $leapworkHelper
Invoke-LeapworkGit add .gitignore README.md RELEASE_NOTES.md 'Abrir caderno.cmd' site scripts research
& git --git-dir=.publication/git --work-tree=. diff --cached --quiet
if ($LASTEXITCODE -eq 1) {
    Invoke-LeapworkGit commit -m "Publica caderno de estudo Leapwork $Version"
} elseif ($LASTEXITCODE -ne 0) { throw 'Não foi possível verificar as alterações.' }
# Push normal: nunca substitui o histórico remoto à força.
Invoke-LeapworkGit push -u origin main
& git --git-dir=.publication/git --work-tree=. rev-parse --verify --quiet "refs/tags/$Version"
if ($LASTEXITCODE -ne 0) { Invoke-LeapworkGit tag -a $Version -m "Caderno de estudo Leapwork $Version" }
Invoke-LeapworkGit push origin "refs/tags/$Version"
$leapworkAssets = @(
    "dist/LeapworkKnowledgeBase-$Version-completo.zip",
    "dist/LeapworkKnowledgeBase-$Version-essencial.zip",
    'dist/SHA256SUMS.txt'
)
& $leapworkGh release view $Version --repo $leapworkRepo --json isDraft 2>$null
if ($LASTEXITCODE -ne 0) {
    Invoke-LeapworkGh release create $Version --repo $leapworkRepo --verify-tag --draft --title "$Version · Caderno de estudo Leapwork" --notes-file RELEASE_NOTES.md
}
Invoke-LeapworkGh release upload $Version @leapworkAssets --repo $leapworkRepo --clobber
Invoke-LeapworkGh release edit $Version --repo $leapworkRepo --draft=false --latest
Invoke-LeapworkGh release view $Version --repo $leapworkRepo --json 'url,isDraft,assets'
