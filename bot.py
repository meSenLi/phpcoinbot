import calculation
import os
import telebot
import network as nk

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


def handleReportadv():
    addresses = ["Pst5VEoCwbeowUoEPLc4iQQvgVKJqSJi3N", "PbyMrPqPKW7rsWgRUKoAsxi56MVan8JVod",
                 "PaNPX1HHMNjLZEYkrDH5nrtW2xjkz7aGnX", "PoAayrZyMWnT3HpnKXRkUJMpApuPsM6rwN",
                 "PhQmzQzv4EvH1jSE5xpggbD1n7ASazaYia"]
    network = nk.Network(
        "https://main1.phpcoin.net/apps/explorer/address.php?address=")
    string = ""
    for address, i in zip(addresses, range(len(addresses))):
        type = "Reward Masternode"
        if i > 2:
            type = "Reward Stake"
        wallet = network.fetchData(address)
        string = string + address + "\n"
        string = string + "  balance:" + str(wallet.Balance)+"\n"
        string = string + "  todayIncom:" + \
            str(wallet.getTodayReward(type=type))+"\n"
        string = string + "  5AvgConf:" + \
            str(wallet.getTypeAverageBlock(type, 5))+"\n"
        string = string + "  10AvgConf:" + \
            str(wallet.getTypeAverageBlock(
                type, 10))+"\n"
        string = string + "  allAvgConf:" + \
            str(wallet.getTypeAverageBlock(type))+"\n"
        string = string + "\n"
    print(string)
    return string


def handleReportAvg():
    addresses = []
    lines = open("address", 'r').readlines()
    for line in lines:
        addresses.append(line.strip())
    wallets = []
    network = nk.Network(
        "https://main1.phpcoin.net/apps/explorer/address.php?address=")
    for address in addresses:
        wallets.append(network.fetchData(address))
    string = "50 2000 average\n"
    balance = 0.0
    income = 0.0
    fiveAvgConf = 0.0
    tenAvgConf = 0.0
    allAvgConf = 0.0
    for wl in wallets[:50]:
        balance = balance + wl.Balance
        income = income + wl.getTodayReward("Reward Stake")
        fiveAvgConf = fiveAvgConf + wl.getTypeAverageBlock("Reward Stake", 5)
        tenAvgConf = tenAvgConf + wl.getTypeAverageBlock("Reward Stake", 10)
        allAvgConf = allAvgConf + wl.getTypeAverageBlock("Reward Stake")
    string = string + "  balance:" + str(balance/50) + "\n"
    string = string + "  todayIncome:" + str(income/50) + "\n"
    string = string + "  5AvgConf:" + str(fiveAvgConf/50) + "\n"
    string = string + "  10AvgConf:" + str(tenAvgConf/50) + "\n"
    string = string + "  allAvgConf:" + str(allAvgConf/50) + "\n"
    string = string + "\n"

    string = string + "25 400 average\n"
    balance = 0
    income = 0.0
    fiveAvgConf = 0
    tenAvgConf = 0
    allAvgConf = 0
    for wl in wallets[50:]:
        balance = balance + wl.Balance
        income = income + wl.getTodayReward("Reward Stake")
        fiveAvgConf = fiveAvgConf + wl.getTypeAverageBlock("Reward Stake", 5)
        tenAvgConf = tenAvgConf + wl.getTypeAverageBlock("Reward Stake", 10)
        allAvgConf = allAvgConf + wl.getTypeAverageBlock("Reward Stake")
    string = string + "  balance:" + str(balance/25) + "\n"
    string = string + "  todayIncome:" + str(income/25) + "\n"
    string = string + "  5AvgConf:" + str(fiveAvgConf/25) + "\n"
    string = string + "  10AvgConf:" + str(tenAvgConf/25) + "\n"
    string = string + "  allAvgConf:" + str(allAvgConf/25) + "\n"
    print(string)
    return string


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['report'])
def send_welcome(message):
    bot.reply_to(message, handleReportadv() + handleReportAvg())


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, handle(message.text))


bot.infinity_polling()
