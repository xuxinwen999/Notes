## Non-structued data

### PDF

#### **Main Types of PDF Files**
* **Text-Based PDFs**: These contain searchable and selectable text, often generated directly from digital sources like word processors.
* **Image-Based PDFs** (Scanned PDFs): These consist of images of text or graphics, typically produced by scanning physical documents. The content is not directly selectable or searchable without processing.
* **Hybrid PDFs**: These combine both text and image elements, such as a scanned document with an embedded text layer added through Optical Character Recognition (OCR).

#### **Main Technical Approaches Overview**
* **OCR-based Text Extraction**. This approach uses OCR models to directly extract text from documents. While feasible for **plain text documents**, it introduces significant noise when documents contain images, tables, formulas, and other elements(主要应用于提取text), rendering it unsuitable for high-quality data extraction.
```
How OCR works to convert images of text(scanned):
    1. Image Analysis: OCR software examines each page of the scanned PDF to detect characters, words, and text lines within the images.
    2. Text Recognition: The software interprets the identified shapes as specific characters or symbols, effectively "reading" the text content.
    3. Text Layer Creation: An invisible text layer is generated, aligning accurately with the original image content. This layer is overlaid on the images but remains hidden from view.
    4. Searchability and Selectability: With the text layer in place, users can search for keywords, select text, and copy content directly from the PDF, even though the visible portion remains unchanged.
```
* **Library-based Text Parsing**. For non-scanned documents, open-source Python libraries such as pypdf, and PyMuPDF can directly read content without invoking OCR, offering **faster** and more accurate text results. However, this approach **fails** when documents contain formulas, tables, and other elements.
* **Multi-Module Document Parsing**. This approach employs various document parsing models to process document images in multiple stages. Initially, layout detection algorithms identify different types of regions, such as images, image captions, tables, table captions, headings, and text. Subsequently, different recognizers are applied to these specific regions. For instance, OCR is used for text and headings, formula recognition models handle formulas, and table recognition models process tables.
* **End-to-End MLLM Document Parsing**.  These models benefit from continuously optimized encoders(e.g., SwinTransformer, ViTDet) and decoders (e.g., mBART, Qwen2-0.5B) as well as data engineering, gradually improving extraction performance. (摘自2024 MinerU report, 该方向待细看)

#### **Multi-Module Document Parsing Based-Approach**
In industry practice, we have to deal with intricate pdf files. Designing versatile workflow is crucial. 下以202409版MinerU report所述的workflow梳理重要的stages and modules:
* Document Preprocessing
    1. filter out unprocessable PDFs, such as non-PDF files, encrypted documents, and password-protected documents.
    2. Obtain PDF metadata: 
        * Language Identification (a parameter when performing
OCR); 
        * Content Garbled Detection; 
        * Scanned PDF Identification (text-based pdf可直接应用pypdf等lib提取text, 而scanned pdf要上ocr)； 
        * Page Metadata Extraction: total page count, page dimensions (width and height), and other relevant attributes.
* Document Content Parsing: MinerU中包括layout detection, formula detection, table recognition, formula recognition and OCR
    1. layout detection: distinguish different types of elements and their corresponding regions on a page. Paper-type documents 比较容易但是在 textbooks and
exam papers等文件上可能需要构造训练数据调整模型
    2. Formula detection: Inner formular(应该是指不单独成行，嵌在text中间的)是一个难点，if formulas are not detected in advance, subsequent text extraction using OCR or Python libraries may result in garbled text. (MinerU也精调了模型)
    3. Formula Recognition: 除了Inner formular, hand-written formula也是一个难点.
    4. Table Recognition: 有不同的table识别方式，如分步骤的TableMaster: divides the table recognition task into four sub-tasks including table structure recognition, text line detection, text line recognition, and box assignment. 也有end-to-end manner, 如StructEqTable.
    5. OCR: 一个难点是text from different columns being recognized as a single column. 有效的解决方案是在layout analysis后将OCR应用于text regions, 而非直接全文应用ocr.
* Document Content Post-Processing: 组织排版前一步解析出的不同regions内容，主要难点是解析后可能产生overlaps, it focuses on handling the relationships between Bounding Boxes