// // Change this to the ID of the list when set
// var list = document.getElementById('myList');

// // Get all the list items in the list
// var items = list.getElementsByTagName('li');

// // Loop through each list item
// for (var i = 0; i < items.length; i++) {
//   // Add a click event listener to the current list item
//   items[i].addEventListener('click', function() {
//     // Check the current value of the text-decoration property
//     if (this.style.textDecoration === 'line-through') {
//       // If it's 'line-through', remove the strikethrough style
//       this.style.textDecoration = 'none';
//     } else {
//       // Otherwise, add the strikethrough style
//       this.style.textDecoration = 'line-through';
//     }
//   });
// }

function toggleStrikeThrough(itemId) {
  var label = document.querySelector('label[for="' + itemId + '"]');
  label.style.textDecoration = label.style.textDecoration === 'line-through' ? 'none' : 'line-through';}

  window.onload = function() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
      checkbox.checked = false;
    });
  };
