

class Authentication:
    #posible logintype
    MetaMask = 1
    Coinbase_Wallet = 2
    WalletConn = 3
    Trust_Wallet = 4
    Fortmatic = 5
    Email_password = 6
    Google = 7
    Facebook = 8

    @staticmethod
    def FetchWalletType(wt):

        if wt == 'Metamask':
            return Authentication.MetaMask
        elif wt == 'Wallet_Connect':
            return Authentication.WalletConn
        elif wt == 'Fortmatic':
            return Authentication.Fortmatic
        elif wt == 'Coinbase':
            return Authentication.Coinbase_Wallet
        elif wt == 'Google':
            return Authentication.Google
        elif wt == 'Facebook':
            return Authentication.Facebook




