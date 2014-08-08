var path = require('path');
var fs = require('fs');
var nsg = require('node-sprite-generator');
var Handlebars = require('handlebars');

nsg({
  src: ['sprites/flair/*.png'],
  spritePath: 'build/images/flair.png',
  stylesheetPath: 'build/css/flair.css',
  layout: 'vertical',
  stylesheet: create_stylesheet('templates/flair.tpl'),
  stylesheetOptions: {
    prefix: 'flair-'
  }
}, function(err) {
  if(err) throw err;
  console.log('done');
});

function create_stylesheet(file) {
    var source = fs.readFileSync(file, 'utf8');
    var template = Handlebars.compile(source);

    return function stylesheet(layout, filepath, spritepath, options, callback) {

        layout.images = layout.images.map(function(image) {
          image['className'] = options.prefix + path.basename(image.path, path.extname(image.path));
          return image;
        });

        var data = {
          'layout': layout,
          'spritepath': spritepath
        }

        fs.writeFile(filepath, template(data), callback);
    };


}

Handlebars.registerHelper('imageurl', imageurl_helper);
Handlebars.registerHelper('pixel', pixel_helper);

function pixel_helper(context, options) {
    var value = parseInt(context, 10);
    if(options.hash['plus'])
      value += parseInt(options.hash['plus'], 10);
    return value+'px'
};

function imageurl_helper(context, options) {
  return '%%'+path.basename(context, path.extname(context))+'%%';
};
