// const PdfReader = require("pdfreader/PdfReader");

// new PdfReader().parseFileItems("pdf2.pdf", function (err, item) {
//   if (err) {
//     console.error(err);
//   }
//   else if (!item) {
//     console.log('ehreere', item);
//   }
//   else if (item.text) console.log(item);
// });

const fs = require('fs');
PDFParser = require("pdf2json");
const pdf = require('pdf-parse');

// const pdfParser = new PDFParser();

// pdfParser.on("pdfParser_dataError", errData => console.error(errData.parserError));
// pdfParser.on("pdfParser_dataReady", pdfData => {
//   console.log(pdfData);
//   fs.writeFile("./pdf2json.json", JSON.stringify(pdfData), () => {});
// });

// pdfParser.loadPDF("./pdf3.pdf");


let dataBuffer = fs.readFileSync('pdf3.pdf');

pdf(dataBuffer).then(function (data) {

  // // number of pages
  // console.log('here', data.numpages);
  // // number of rendered pages
  // console.log('here1', data.numrender);
  // // PDF info
  // console.log(data.info);
  // // PDF metadata
  // console.log(data.metadata);
  // // PDF.js version
  // // check https://mozilla.github.io/pdf.js/getting_started/
  // console.log(data.version);
  // // PDF text
  // console.log(data.text);
  console.log(data);

})