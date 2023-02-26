var escodegen = require('escodegen');
var a = require('./mytscode.json');
var js = escodegen.generate(a);
console.log(js);