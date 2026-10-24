param([string]$OutputDirectory = 'docs/qa/office-render')
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$renderRoot = [IO.Path]::GetFullPath((Join-Path $projectRoot $OutputDirectory))
if (-not $renderRoot.StartsWith($projectRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw '輸出位置必須位於本專案內。' }
New-Item -ItemType Directory -Force -Path $renderRoot | Out-Null
$results = [Collections.Generic.List[object]]::new()
$word = $null
$powerpoint = $null
$excel = $null
try {
    # Word COM 在本機無法完成驗收，預設僅驗證 PowerPoint 與 Excel。
    if ($env:OFFICE_KIT_INCLUDE_WORD -eq '1') {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $wordFiles = Get-ChildItem -LiteralPath (Join-Path $projectRoot 'examples') -Filter '*.docx' -Recurse | Where-Object { $_.Directory.Name -eq 'output' }
    foreach ($file in $wordFiles) {
        $doc = $null
        try {
            $doc = $word.Documents.Open($file.FullName, $false, $true, $false)
            $out = Join-Path $renderRoot ($file.Directory.Parent.Name + '-' + $file.BaseName + '.pdf')
            $doc.ExportAsFixedFormat($out, 17)
            $results.Add([PSCustomObject]@{ Source=$file.FullName; Output=$out; Application='Word'; Status='opened-and-exported' })
        } finally { if ($null -ne $doc) { $doc.Close(0); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($doc) } }
    }
    }
    $powerpoint = New-Object -ComObject PowerPoint.Application
    $powerpoint.AutomationSecurity = 3
    $slideFiles = Get-ChildItem -LiteralPath (Join-Path $projectRoot 'examples') -Filter '*.pptx' -Recurse | Where-Object { $_.Directory.Name -eq 'output' }
    foreach ($file in $slideFiles) {
        $deck = $null
        try {
            $deck = $powerpoint.Presentations.Open($file.FullName, -1, 0, 0)
            $out = Join-Path $renderRoot ($file.Directory.Parent.Name + '.pdf')
            $deck.SaveCopyAs($out, 32)
            $slideFolder = Join-Path $renderRoot 'slides'
            New-Item -ItemType Directory -Force -Path $slideFolder | Out-Null
            foreach ($slide in $deck.Slides) {
                $slide.Export((Join-Path $slideFolder ('slide-' + $slide.SlideIndex + '.png')), 'PNG', 1600, 900)
            }
            $results.Add([PSCustomObject]@{ Source=$file.FullName; Output=$out; Application='PowerPoint'; Status='opened-and-exported'; Slides=$deck.Slides.Count })
        } finally { if ($null -ne $deck) { $deck.Close(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck) } }
    }
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AutomationSecurity = 3
    $sheetFiles = Get-ChildItem -LiteralPath (Join-Path $projectRoot 'examples') -Filter '*.xlsx' -Recurse | Where-Object { $_.Directory.Name -eq 'output' }
    foreach ($file in $sheetFiles) {
        $book = $null
        try {
            $book = $excel.Workbooks.Open($file.FullName, 0, $true)
            foreach ($sheet in $book.Worksheets) {
                $sheet.PageSetup.Orientation = 2
                $sheet.PageSetup.Zoom = $false
                $sheet.PageSetup.FitToPagesWide = 1
                $sheet.PageSetup.FitToPagesTall = $false
                $sheet.PageSetup.PrintArea = $sheet.UsedRange.Address()
            }
            $out = Join-Path $renderRoot ($file.Directory.Parent.Name + '.pdf')
            $book.ExportAsFixedFormat(0, $out)
            $results.Add([PSCustomObject]@{ Source=$file.FullName; Output=$out; Application='Excel'; Status='opened-and-exported'; Sheets=$book.Worksheets.Count })
        } finally { if ($null -ne $book) { $book.Close($false); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($book) } }
    }
} finally {
    if ($null -ne $word) { $word.Quit(0); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) }
    if ($null -ne $powerpoint) { $powerpoint.Quit(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($powerpoint) }
    if ($null -ne $excel) { $excel.Quit(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($excel) }
    $results | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $renderRoot 'open-results.json') -Encoding UTF8
}
$results | Select-Object Application,Status,Output
