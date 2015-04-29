var exec = require('child_process').exec;

exec('python asm.py tmp.asm', function(error, stdout, stderr){
  console.log(stdout);
});