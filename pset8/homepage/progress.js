$(function() {
  var current_progress = 0;
  var interval = setInterval(function() {
      if(current_progress <95){
          current_progress += 5;
      }else{
          current_progress += 4;
      }

      $("#dynamic")
      .css("width", current_progress + "%")
      .attr("aria-valuenow", current_progress)
      .text(current_progress + "% Complete");
      if (current_progress >= 99)
          clearInterval(interval);
  }, 800);
});