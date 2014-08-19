var path = require('path');
var fs = require('fs');
var nsg = require('node-sprite-generator');
var Handlebars = require('handlebars');

nsg({
  src: ['sprites/flair/*.png'],
  spritePath: 'images/flair.png',
  stylesheetPath: 'userflair.scss',
  layout: 'vertical',
  stylesheet: create_stylesheet('templates/flair.tpl'),
  stylesheetOptions: {
    prefix: ''
  }
}, function(err) {
  if(err) throw err;
  console.log('done');
});

nsg({
  src: ['sprites/misc/*.png'],
  spritePath: 'images/misc.png',
  stylesheetPath: 'misc.scss',
  layout: 'vertical',
  stylesheet: print_misc,
  stylesheetOptions: {
    prefix: ''
  }
}, function(err) {
  if(err) throw err;
  console.log('done');
});

function print_misc(layout) {
  layout.images.forEach(function(image) {
    var className = path.basename(image.path, path.extname(image.path));
    var x = image.x;
    var y = image.y;
    var width = image.width;
    var height = image.height;
    console.log('%s: background-position: -%spx -%spx; width: %spx; height: %spx;', className, x, y, width, height);
  });
}

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

function create_tilesheet() {
  var tiles = require('./tiles.json');
  var source = fs.readFileSync('./templates/tiles.tpl', 'utf8');
  var template = Handlebars.compile(source);

  tiles = Object.keys(tiles).map(function(tile) {
    var t = tiles[tile]
    if(tile != "marsball")
      return {className: tile, x: t.x * 40, y: t.y * 40, width: 40, height: 40};
    return {className: tile, x: t.x * 40, y: t.y * 40, width: 80, height: 80};
  });

  var data = {
    tiles: tiles,
    spritepath: './images/tiles.png'
  }

  fs.writeFileSync('./tilesheet.scss', template(data));
}
create_tilesheet();

