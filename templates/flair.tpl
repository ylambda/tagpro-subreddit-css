.flair {
  background: url('{{#imageurl spritepath}}{{/imageurl}}') no-repeat;
  border: none !important;
  line-height: 16px;
}
{{#each layout.images}}
.{{ className }} {
  background-position: -{{#pixel x}}{{/pixel}} -{{#pixel y}}{{/pixel}};
  width: auto;
  padding-left: {{#pixel width plus="2"}}{{/pixel}};
  height: {{#pixel height}}{{/pixel}};
}
{{/each}}
