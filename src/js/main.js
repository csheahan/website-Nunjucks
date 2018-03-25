function setRandomHomepageBackground() {
  var backgrounds = [
    "genericMountainBackground.jpg",
    "angkorWatBackground.jpg",
    "lotusPlants.jpg",
    "yamazakiDistillery.jpg"
  ];

  var picNum = Math.floor(Math.random() * 4);

  $('header').css('background-image', 'url(./img/index_backgrounds/' + backgrounds[picNum] + ')');
}

$(document).ready(function() {
  setRandomHomepageBackground();
});
