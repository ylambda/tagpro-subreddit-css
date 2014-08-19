.flair {
  background: url('{{#imageurl spritepath}}{{/imageurl}}') no-repeat;
  border: none !important;
  line-height: 16px;
}
{{#each layout.images}}
.flair-{{ className }} {
  background-position: -{{#pixel x}}{{/pixel}} -{{#pixel y}}{{/pixel}};
  width: auto;
  padding-left: {{#pixel width plus="2"}}{{/pixel}};
  height: {{#pixel height}}{{/pixel}};
}
{{/each}}

/* flair in image */

.md a[href^="#flair-"] {
  background: url('{{#imageurl spritepath}}{{/imageurl}}') no-repeat;
  border: none !important;
  line-height: 16px;
  display: inline-block;
  cursor: default;
}

{{#each layout.images}}
.md a[href^="#flair-{{ className }}"] {
  background-position: -{{#pixel x}}{{/pixel}} -{{#pixel y}}{{/pixel}};
  width: {{#pixel width }}{{/pixel}};
  height: {{#pixel height}}{{/pixel}};
}
{{/each}}
