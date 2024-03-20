document.addEventListener('DOMContentLoaded', () => {
    const terminalContent = document.getElementById('terminal-content');
    const commandInput = document.getElementById('command-input');
    let commandHistory = [];
    let historyIndex = -1;

    commandInput.focus();

    const typeText = (text, clear = false) => {
        if (clear) terminalContent.innerHTML = '';
        let index = 0;
        const speed = 10; // Typing speed in milliseconds
        const typeCharacter = () => {
            if (index < text.length) {
                if (text.charAt(index) === '\n') {
                    terminalContent.innerHTML += '<br>';
                } else {
                    terminalContent.innerHTML += text.charAt(index);
                }
                index++;
                setTimeout(typeCharacter, speed);
            }
        };
        typeCharacter();
    };

    const initialMessage = "Welcome to Cyntax Error. A place of software excellence and software solutions.\nType 'help' for a list of commands and services.";
    typeText(initialMessage);

    const handleCommand = (command) => {
        commandHistory.push(command);
        historyIndex = commandHistory.length;
        switch (command.toLowerCase()) {
            case 'help':
                const helpText = "List of available commands:\n- help - Display available commands\n- clear - Clear the terminal\n- bio - Tells you a little about myself\n- contact - Contact information\n- projects - See project examples";
                typeText(helpText, true);
                break;
            case 'clear':
                terminalContent.innerHTML = '';
                break;
            case 'bio':
                // Assuming loadContent is defined to fetch and display content
                loadContent('bio');
                break;
            case 'contact':
                // Assuming loadContent is defined to fetch and display content
                loadContent('contact');
                break;
            case 'projects':
                // Assuming loadContent is defined to fetch and display content
                loadContent('projects');
                break;
            default:
                typeText(`${command}: command not found`, true);
        }
    };

    commandInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            const command = commandInput.value.trim();
            if (command !== '') {
                handleCommand(command);
            }
            commandInput.value = '';
        } else if (event.key === 'ArrowUp') {
            if (historyIndex > 0) {
                historyIndex--;
                commandInput.value = commandHistory[historyIndex];
            }
            event.preventDefault(); // Prevent the cursor from moving to the start of the input
        } else if (event.key === 'ArrowDown') {
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                commandInput.value = commandHistory[historyIndex];
            } else {
                commandInput.value = '';
            }
            event.preventDefault(); // Prevent the cursor from moving to the end of the input
        }
    });

    // Load content dynamically
    const loadContent = (filename) => {
        // Placeholder for content loading logic
        // Use fetch API or similar to load content dynamically
        console.log(`Loading content for: ${filename}`);
        // Example: fetch(`/content/${filename}.txt`).then...
    };
});
