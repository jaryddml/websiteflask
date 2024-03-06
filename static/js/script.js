document.addEventListener('DOMContentLoaded', () => {
    // Get terminal elements
    const terminalContent = document.getElementById('terminal-content');
    const commandInput = document.getElementById('command-input');

    // Set focus to command input field
    commandInput.focus();

    // Typing effect for welcome text
    const welcomeText = "Welcome to Cyntax Error. A place of software excellence and software solutions.\nType 'help' for a list of commands and services.";
    typeText(welcomeText); // Apply typing effect to welcome message

    // Handle command input
    commandInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            const command = commandInput.value.trim();
            handleCommand(command);
            commandInput.value = ''; // Clear command input
        }
    });
});

// Function to handle entered commands
function handleCommand(command) {
    const terminalContent = document.getElementById('terminal-content');

    // Display entered command
    const commandLine = document.createElement('div');
    commandLine.innerHTML = `<span id="prompt">$</span> ${command}`;
    terminalContent.appendChild(commandLine);

    // Execute command
    switch (command.toLowerCase()) {
        case 'help':
            const helpText = "List of available commands:\n- help - Display available commands\n- clear - Clear the terminal\n- bio - Tells you a little about myself\n- contact - Contact information\n- projects - See project examples";
            typeText(helpText); // Apply typing effect to command output
            break;
        case 'clear':
            terminalContent.innerHTML = ''; // Clear terminal content
            break;
        case 'bio':
            const bioText = "Jaryd: Your Trusted Software Architect, Built for Efficiency.\n\nMy Story: I'm Jaryd, a passionate software developer with a unique blend of business acumen and technical expertise. My journey began in retail management, where I honed my ability to identify customer needs and translate them into actionable solutions. This experience has become a cornerstone of my development approach, allowing me to understand your challenges and craft efficient software solutions that directly address them.\n\nWhat I Offer:\n- Strategic Consulting: My background in retail provides valuable insights, allowing me to collaborate with you to understand your business goals and translate them into a clear technical roadmap.\n- Technical Expertise: I'm proficient in various programming languages and frameworks, ensuring I can build robust and scalable solutions tailored to your specific needs.\n- Focus on Efficiency: I understand the importance of minimizing your project costs and timeframes. I prioritize clean code, efficient development practices, and clear communication to ensure your project stays on track and within budget.\n\nWhy Choose Me?\n- Client-Centric Approach: I prioritize understanding your business goals and tailoring solutions that seamlessly integrate with your existing infrastructure and processes.\n- Flexibility & Adaptability: I thrive in fast-paced environments and adapt to your specific needs, whether it's short-term project completion or long-term partnerships.\n- Passion & Dedication: I'm genuinely passionate about software development and committed to delivering the best possible solutions for your business.\n\nInvest in Efficiency. Contact Jaryd today!";
            typeText(bioText); // Apply typing effect to command output
            break;
        case 'contact':
            const contactText = "Contact Information:\n- Email: jaryddml@gmail.com\n- LinkedIn: https://www.linkedin.com/in/jaryd-lloyd-9318b722a/ \n- GitHub: github.com/jaryddml\n\nFeel free to contact me at anytime with any questions you may have.\n My response times are typically within one to two business days.\nI look forward to hearing from you.\n";
            typeText(contactText); // Apply typing effect to command output
            break;
        case 'projects':
            const projectsText = "Project examples will be available in the future. Stay tuned!";
            typeText(projectsText); // Apply typing effect to command output
            break;
        default:
            const errorText = `${command}: command not found`;
            typeText(errorText); // Apply typing effect to command output
    }

    // Scroll to bottom of terminal
    terminalContent.scrollTop = terminalContent.scrollHeight;
}

// Function to apply typing effect to text
function typeText(text) {
    const terminalContent = document.getElementById('terminal-content');
    const typingSpeed = 10; // Adjust typing speed (milliseconds)
    let index = 0;

    function typeCharacter() {
        if (index < text.length) {
            const char = text.charAt(index);
            if (char === '\n') {
                terminalContent.innerHTML += '<br>';
            } else {
                terminalContent.innerHTML += char;
            }
            index++;
            setTimeout(typeCharacter, typingSpeed);
        }
    }

    typeCharacter();
}