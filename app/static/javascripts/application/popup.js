function Popup() {
  this.html     = $('html');
  this.overlay  = $('.popup-overlay');
  this.content  = $('.popup-content');
  this.loader   = $('.popup-loader-container');
  this.done     = $('.popup-certificate');

  this.bindArgee();
  this.bindClose();
}

Popup.prototype = {
  bindArgee: function() {
    var self = this;
    $('.agree').on('click', function() {
      self.open();
    });
  },

  bindClose: function() {
    var self = this;
    $('.popup-certificate-close').on('click', function() {
      self.close()
    });
  },

  process: function() {
    var self = this;
    setTimeout(function() {
      self.loader.hide();
      self.done.css('display', 'inline-block');
    }, 3000);
  },

  open: function() {
    this.overlay.addClass('popup-overlay_show');
    this.html.addClass('hidden');
    this.process();
  },

  close: function() {
    this.overlay.removeClass('popup-overlay_show');
    this.html.removeClass('hidden');
  }
}

$(function() {
  new Popup
});
