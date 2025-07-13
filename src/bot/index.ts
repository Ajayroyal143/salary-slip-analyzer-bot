// This file is the entry point for the bot. It initializes the bot and sets up the necessary configurations and event listeners.

import { SalarySlipAnalyzer } from '../analyzer/salarySlipAnalyzer';
import { initializeBot } from './botInitializer';

const bot = initializeBot();

bot.on('message', (message) => {
    const analyzer = new SalarySlipAnalyzer();
    const result = analyzer.analyzeSalarySlip(message.content);
    bot.sendMessage(message.channel, result);
});

bot.start();