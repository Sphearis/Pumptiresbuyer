# Pump.tires automatic buyer

Pulsechain pump.tires automatic token buyer, buys a token every 10 minutes, 1 hour, 1 day, ...

Pretty simple script I'm publishing because it's very hard to find a starting point into the Pulsechain ecosystem, there are no resources or docs available for most blockchain features.

I created this for me, after a lot of trials and invalid transactions it actually worked!

It can help you as a token creator or as a token buyer. More features are coming (I'm thinking about a multitoken buyer and also automatically buying a small amount of pump.tires token as soon as they're released).

To use it, it's very simple:

Create your python environment and use the following command line to install the requirements
*pip install web3 schedule dotenv*

1) Edit the .env:
-   PULSECHAIN_RPC_URL is where you put the RPC url, the address you will use to send your signed transactions, no key is transferred at this point and nobody can reverse engineer your transaction, it is sent as it is stored on the blockchain, for more information about how that works, please ask an AI about transaction signing. The default RPC is https://rpc.pulsechain.com and it's fine for now, but in case there are a lot of users at some point, you might have to use another more private one (or your own node) for fast and successful transactions.

-  PRIVATE_KEY is where your private key goes, as you can see in the code it's only used internally to sign the transactions. If you're unsure, simply ask someone who knows code.
That key remains on your computer at all times...
But still, please don't use your main address even if it's tempting, create a specific one and start from there, don't forget about the risks of having a private key appearing clearly in a text file. You have to be the responsible one, I can't be blamed if for some reason you don't protect your key sufficiently. Be aware of viruses, keyloggers, clipboard loggers, network hacks, ...

-   ORDER_SIZE is where you set the amount you want to buy in PLS (default is 20000 PLS), don't forget transaction fees are added to it, make orders big enough for it to be worthwhile. At some point you can have to pay 6-700 PLS just for fees but it's usually way lower.

-   TOKEN_ADDRESS is the address of the token you want to buy automatically (default is the address of my own token $FEW that you can buy as a thank you... And maybe to make money in the future :p)
 
2) Send some PLS on that address, the contract call will automatically convert it to WPLS when it'll make a transaction so you don't have to do it. Only PLS is needed for it to work, other tokens or stables can't be used to buy.

Launch the script, by default it will make a trade immediately, you'll be able to see if it works, if you don't want a direct order as soon as you launch the script, you can simply comment this line and it will wait for the specified delay before making a trade:

*job() # Do a buy as soon as the script is launched*

To change the delay, if you want to buy every 10 minutes instead of 1 hour for example (this will be better implemented in the future):

change *schedule.every().hour.do(job)* to *schedule.every(10).minutes.do(job)*

More info about schedule here:
https://schedule.readthedocs.io/en/stable/index.html

