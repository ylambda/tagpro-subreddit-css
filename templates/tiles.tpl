/* tiles in image */

.md a[href^="#tile-"] {
  background: url('{{#imageurl spritepath}}{{/imageurl}}') no-repeat;
  border: none !important;
  line-height: 16px;
  display: inline-block;
  cursor: default;
}

{{#each tiles}}
.md a[href^="#tile-{{ className }}"] {
  background-position: -{{#pixel x}}{{/pixel}} -{{#pixel y}}{{/pixel}};
  width: {{#pixel width }}{{/pixel}};
  height: {{#pixel height}}{{/pixel}};
}
{{/each}}
