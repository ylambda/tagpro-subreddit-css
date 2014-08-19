# Set this to the root of your project when deployed:

http_path = "/"
css_dir = "stylesheets"
sass_dir = "sass"
images_dir = "sprites"
javascripts_dir = "javascripts"
generated_images_dir = "images"

# disable debugging comments
line_comments = false

# dont use the compass hash for filenames
on_sprite_saved do |filename|
    target = filename.sub(/-s[a-f0-9]{10}\.png/, ".png")
    FileUtils.mv(filename, target)
end
