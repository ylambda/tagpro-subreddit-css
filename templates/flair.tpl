.flair {
  background-image: url('<%= options.spritePath %>');
}

<% layout.images.forEach(function (image) { %>.<%= image.className %> {
  background-position: <%= getCSSValue(-image.x) %> <%= getCSSValue(-image.y) %>;
  width: auto;
  padding-left: <%= getCSSValue(image.width) %>;
  height: <%= getCSSValue(image.height) %>;
}
<% }); %>
