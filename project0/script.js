const classNames = {
  TODO_ITEM: 'todo-container',
  TODO_CHECKBOX: 'todo-checkbox',
  TODO_TEXT: 'todo-text',
  TODO_DELETE: 'todo-delete',
}

const list = document.getElementById('todo-list')
const itemCountSpan = document.getElementById('item-count')
const uncheckedCountSpan = document.getElementById('unchecked-count')

function newTodo(){
  //prompt for to do item
  var todo = prompt("Add to do", "to do")

  //count items and add one
  var count = Number(itemCountSpan.innerHTML) + 1

  //create li element
  var li = document.createElement('LI')
  
  // creating checkbox element
  var checkbox = document.createElement('input');
             
  // Assigning the attributes to created checkbox
  var name = "to-do-check_" + count
  var id = count
  checkbox.type = "checkbox";
  checkbox.name = name;
  checkbox.value = todo;
  checkbox.id = count;
    
  // creating label for checkbox
  var label = document.createElement('label');
    
  // assigning attributes for
  // the created label tag
  label.htmlFor = count;
    
  // appending the created text to
  // the created label tag
  label.appendChild(document.createTextNode(todo));
    
  // appending the checkbox
  // and label to div
  li.appendChild(checkbox);
  li.appendChild(label);

  list.appendChild(li)
  itemCountSpan.innerHTML = document.querySelectorAll("li").length
  uncheckedCountSpan.innerHTML = document.querySelectorAll("li").length - document.querySelectorAll('input[type="checkbox"]:checked').length
}

function newTodotest() {

  var count = Number(itemCountSpan.innerHTML) + 1
  itemCountSpan.innerHTML = count

  // add item count
  var todo = prompt("Add to do", "to do")
  var li = document.createElement("LI")
  var check = document.createElement("INPUT")
  check.type = "checkbox"
  checkbox.name = "name";
  checkbox.value = "value";
  checkbox.id = "check"+count
  var label = document.createElement('label')
  label.htmlFor = checkbox.id
  

  label.appendChild(document.createTextNode(todo))
  li.appendChild(check)
  li.appendChild(label)

  list.appendChild(li)

  // add item with check box

  
}
