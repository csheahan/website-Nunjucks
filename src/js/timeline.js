$(document).ready(function() {
  $(".hs").hide();

  $("#highCheck").click(function() {
    if (this.checked) {
      $(".hs").show();
    }
    else {
      $(".hs").hide();
    }
  });

  $("#collegeCheck").click(function() {
    if (this.checked) {
      $(".college").show();
    }
    else {
      $(".college").hide();
    }
  });

  $("#scholarshipCheck").click(function() {
    if (this.checked) {
      $(".scholarship").show();
    }
    else {
      $(".scholarship").hide();
    }
  });

  $("#internCheck").click(function() {
    if (this.checked) {
      $(".intern").show();
    }
    else {
      $(".intern").hide();
    }
  });
});