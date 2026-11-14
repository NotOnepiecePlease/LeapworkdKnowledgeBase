# Downloads dos 48 vídeos das aulas disponíveis nos módulos 1, 2 e 3.
# Legendas originais são obtidas separadamente para que uma falha de
# legendas não interrompa o download do arquivo de vídeo.
$ErrorActionPreference = 'Stop'
$leapworkRoot = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $leapworkRoot 'tools'
$leapworkVideos = @('d9m4N9sxFT0', '9IdcfvVSKAc', 'qHp1RY9AQds', 'M-y1MxK3_Dw', 'pZAVmupXWhE', 'aGduKxCIZAk', '-51LTRplY48', 'TXWo3qK9Oy8', '23YBj_t1EjA', 'ynF7HY2ux_c', 'sJ3Fa3kSiJg', 'qGGNbk0UY-0', 'fO6aVmNKUCc', 'akmkQk8sc40', 'rK8qIFccfbk', 'AL_LQQ4yMLc', 'xAl2LfFKxj0', 'lsGjkso3Rbg', 'lb78WgJ0-wo', 'suIDRArjQEk', '3M0KO_fi8WY', 'r8IH1LYegOo', 'gERnZ6rN1VQ', 'TCcN6YORYC0', 'YP3TJrud2BY', 'c56VBmlFSC0', 'Cd4rHHq2OZY', 'bM5smmLOsBs', 'Xw2nXTOe9NE', '_t-g5jxOdno', '5SALJ43raC4', 'I4rIpx-xlic', 'vbz5ckcdb-Y', 'oke1UlnrP0c', '47VeVtNuyFk', 'SiZZut-jgiY', 'c3aFyb7pRIE', '36KXvQRsMq4', 'Mg-1NKCuf3g', 'I_BUzm8rJ0I', 'N8utEzbs2SM', 'X9Em1PtM9XU', 'B98UeOK1CTU', 'lBcRNry3bo8', 'V5r-Fovn_vs', 'HWUVg1tTclg', '3ALOfIs_OTY', 'J-ui6FyDkXg')
$leapworkTemplate = Join-Path $leapworkRoot 'videos\%(id)s.%(ext)s'
foreach ($leapworkId in $leapworkVideos) {
    $leapworkUrl = "https://www.youtube.com/watch?v=$leapworkId"
    python -m yt_dlp --ignore-config --no-playlist --js-runtimes node --socket-timeout 25 --retries 2 --no-progress --no-overwrites -f 'bv*[height<=1080]+ba/b[height<=1080]' --merge-output-format mp4 --write-info-json --windows-filenames -o $leapworkTemplate $leapworkUrl
    if ($LASTEXITCODE -ne 0) { throw "Falha ao obter o vídeo $leapworkId" }
    $leapworkCaption = Join-Path $leapworkRoot "videos\$leapworkId.en-orig.vtt"
    if (-not (Test-Path -LiteralPath $leapworkCaption)) {
        python -m yt_dlp --ignore-config --no-playlist --js-runtimes node --skip-download --write-auto-subs --sub-langs en-orig --sub-format vtt -o $leapworkTemplate $leapworkUrl
        if ($LASTEXITCODE -ne 0) { Write-Warning "Vídeo salvo; legenda original não disponível para $leapworkId" }
    }
}
