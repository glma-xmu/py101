# Run locally with Microsoft PowerPoint installed. Originals are opened read-only.
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$inputRoot = Join-Path $projectRoot 'resource/projects'
$renderRoot = Join-Path $inputRoot '.previews'
New-Item -ItemType Directory -Force -Path $renderRoot | Out-Null
$powerpoint = New-Object -ComObject PowerPoint.Application
$records = @()
$previous = @()
if (Test-Path (Join-Path $renderRoot 'sources.json')) { $previous = Get-Content -Raw (Join-Path $renderRoot 'sources.json') | ConvertFrom-Json }
try {
    foreach ($cohort in @('26S', '25S', '24S')) {
        $number = 0
        foreach ($file in (Get-ChildItem -LiteralPath (Join-Path $inputRoot $cohort) -File | Sort-Object Name)) {
            if ($file.Extension -notin @('.pptx', '.pdf')) { continue }
            $number++
            $id = "$($cohort.ToLower())-$('{0:d2}' -f $number)"
            $cached = $previous | Where-Object { $_.cohort -eq $cohort -and $_.source -eq $file.Name } | Select-Object -First 1
            if ($cached) { $id = $cached.id }
            else {
                while (($previous | Where-Object { $_.id -eq $id }) -or ($records | Where-Object { $_.id -eq $id })) {
                    $number++
                    $id = "$($cohort.ToLower())-$('{0:d2}' -f $number)"
                }
            }
            $output = Join-Path $renderRoot $id
            if ($cached -and (Test-Path (Join-Path $output "$($cached.count).png"))) { $records += $cached; continue }
            New-Item -ItemType Directory -Force -Path $output | Out-Null
            $record = @{ id=$id; cohort=$cohort; source=$file.Name; title=''; count=0 }
            if ($file.Extension -eq '.pptx') {
                try { $deck = $powerpoint.Presentations.Open($file.FullName, -1, 0, 0) }
                catch { Write-Warning "Cannot render $($file.FullName): $_"; continue }
                try {
                    $record.count = $deck.Slides.Count
                    $texts = @()
                    foreach ($shape in $deck.Slides.Item(1).Shapes) {
                        if ($shape.HasTextFrame -and $shape.TextFrame.HasText) { $texts += $shape.TextFrame.TextRange.Text }
                    }
                    $record.title = $texts -join ' | '
                    for ($i=1; $i -le $deck.Slides.Count; $i++) {
                        $height = [int](1440 * $deck.PageSetup.SlideHeight / $deck.PageSetup.SlideWidth)
                        $deck.Slides.Item($i).Export((Join-Path $output "$i.png"), 'PNG', 1440, $height)
                    }
                } finally { $deck.Close() }
            } else {
                & pdftoppm -scale-to 1440 -png $file.FullName (Join-Path $output 'page')
                if ($LASTEXITCODE -ne 0) { throw "PDF rendering failed: $($file.Name)" }
                $pages = Get-ChildItem -LiteralPath $output -Filter 'page-*.png' | Sort-Object { [int]($_.BaseName -replace 'page-', '') }
                $record.count = $pages.Count
                $i=0
                foreach ($page in $pages) {
                    $i++
                    for ($attempt=1; $attempt -le 5; $attempt++) {
                        try {
                            Move-Item -LiteralPath $page.FullName -Destination (Join-Path $output "$i.png") -Force
                            break
                        } catch {
                            if ($attempt -eq 5) { throw }
                            Start-Sleep -Seconds 1
                        }
                    }
                }
            }
            $records += $record
            Write-Output "$id $($file.Name): $($record.count) slides"
            $records | ConvertTo-Json -Depth 4 | Set-Content -Encoding utf8 (Join-Path $renderRoot 'sources.json')
        }
    }
    $records | ConvertTo-Json -Depth 4 | Set-Content -Encoding utf8 (Join-Path $renderRoot 'sources.json')
} finally { $powerpoint.Quit() }
