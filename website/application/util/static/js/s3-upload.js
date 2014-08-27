// Make sure to include this before the main .js code to ensure the button validation gets activated properly
$(function() {

  // To enable validation of our Semantic UI "button" as a div
  $.fn.form.settings.selector.field += ', div'

  function getSanitizedData(form) {
    var fullData = form.find('input').toArray();
    var publicData = $.grep(fullData, function(element, index) { return element.name.indexOf('x-amz-meta-')===0; }, true);
    var formData = $.grep(publicData, function(element, index) { return element.name==="file"; }, true);
    return formData;
  }
  $('.s3.upload.form').each(function() {
    var form = $(this);

    var button = form.find('div[class*=s3][class*=upload][class*=button]');
    button.click(function() {
      form.find('input[type=file]').click();
    });
    button.text("Upload " + button.text());

    var result = form.find("h4");

    form.fileupload({
      autoUpload: true,
      dataType: 'xml',
      url: form.find('input[name=x-amz-meta-bucket_url]').val(),
      formData: getSanitizedData(form),
      add: function(event, data) {
        result.parent('.field').slideUp();
        var policyEndpoint = form.find('input[name=x-amz-meta-policy_endpoint]').val();
        $.get(policyEndpoint).done(function(params) {
          form.find('input[name=key]').val(params.key);
          form.find('input[name=policy]').val(params.policy);
          form.find('input[name=signature]').val(params.signature);
          data.submit();
        });
      },
      done: function(event, data) {
        button.addClass('completed');
        if (button.text().indexOf('new')===-1) {
          button.text(button.text().replace('Upload', 'Upload new'));
        }
        result.parent('.field').slideDown();
        if (form.hasClass('error')) {
          form.parent('.form').form('validate form');
        }
      }
    });
  });
});
