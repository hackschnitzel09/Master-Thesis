const requestUrl = "http://127.0.0.1:8080/tasks";
const messageDiv = document.getElementById('message');

const taskManagerTitle = document.querySelector('h1');

// Dynamically set task manager title based on requestUrl
if (requestUrl.includes('8080')) {
    taskManagerTitle.innerHTML += ' (amqp)';
} else if (requestUrl.includes('5011')) {
    taskManagerTitle.innerHTML += ' (api)';
}

function fetchAndPrintTasks() {
    fetch(requestUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const tasksDiv = document.getElementById('tasks');
            tasksDiv.innerHTML = '';
            if (Array.isArray(data)) {
                data.forEach(task => {
                    tasksDiv.innerHTML += createHTMLForTask(task);
                });
            } else {
                tasksDiv.innerHTML += createHTMLForTask(data);
            }
        })
        .catch(error => {
            displayMessage('Error fetching tasks: ' + error.message, 'error');
        });
}

function createHTMLForTask(task) {
    let html = '<div>';
    for (const key in task) {
        if (task.hasOwnProperty(key)) {
            html += `<strong>${key}</strong>: `;
            const value = task[key];
            if (typeof value === 'object') {
                html += createHTMLForObject(value);
            } else {
                html += value + '<br>';
            }
        }
    }
    html += '</div><hr>';
    return html;
}

function createHTMLForObject(obj) {
    let html = '<ul>';
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            html += `<li><strong>${key}</strong>: `;
            const value = obj[key];
            if (typeof value === 'object') {
                html += createHTMLForObject(value);
            } else {
                html += value;
            }
            html += '</li>';
        }
    }
    html += '</ul>';
    return html;
}

function addTask() {
    const newTaskTitle = document.getElementById('newTaskInput').value.trim();
    if (newTaskTitle === '') {
        displayMessage('Task title cannot be empty', 'error');
        return;
    }
    fetch(requestUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: newTaskTitle })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error adding task');
        }
        return response.json();
    })
    .then(data => {
        displayMessage(data.message, 'success');
        fetchAndPrintTasks();
    })
    .catch(error => {
        displayMessage('Error adding task: ' + error.message, 'error');
    });
}

function editTask() {
    // Code für das Bearbeiten eines Tasks
    const taskId = document.getElementById('taskIdInput').value;
    
    // Fetch the current task to get its title
    fetch(`${requestUrl}/${taskId}`)
        .then(response => {
            if (!response.ok) {
                alert(response.status + " Task not found")
                throw new Error('Task not found');
            }
            return response.json();
        })
        .then(task => {
            const currentTitle = task.title;
            const newTaskTitle = prompt("Enter new task title:", currentTitle);
            
            if (newTaskTitle === null || newTaskTitle === '') {
                return; // If user cancels or enters empty title, do nothing
            }
            
            // Send PUT request to update task title
            fetch(`${requestUrl}/${taskId}`, {
                method: 'PUT',
               // mode: 'no-cors',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: newTaskTitle })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error editing task');
                }
                // Reload tasks after editing
                fetchAndPrintTasks();
            })
            .catch(error => {
                console.error('Error editing task:', error);
            });
        })
        .catch(error => {
            console.error('Error fetching task:', error);
        });
}

function deleteTask() {
    // Code für das Löschen eines Tasks
    const taskId = document.getElementById('taskIdInput').value;
    fetch(`${requestUrl}/${taskId}`, {
        method: 'DELETE',
        //mode: 'no-cors'
    })
    .then(response => {
        if (!response.ok) {
            alert(response.status + " Task not found")
            throw new Error('Error deleting task');
        } 
        // Reload tasks after deletion
        fetchAndPrintTasks();
    })
    .catch(error => {
        console.error('Error deleting task:', error);
    });
}

function displayMessage(message, type) {
    messageDiv.textContent = message;
    messageDiv.className = type;
    setTimeout(() => {
        messageDiv.textContent = '';
        messageDiv.className = '';
    }, 3000);
}

fetchAndPrintTasks();
