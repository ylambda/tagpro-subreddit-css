var nsg = require('node-sprite-generator');

console.log(__dirname + 'templates/flair.tpl');

nsg({
  src: ['sprites/flair/*.png'],
  spritePath: 'build/images/flair.png',
  stylesheetPath: 'build/css/flair.css',
  layout: 'diagonal',
  stylesheet: 'templates/flair.tpl',
  stylesheetOptions: {
    prefix: 'sprite-'
  }
}, function(err) {
  if(err) throw err;
  console.log('done');
});
