import akshare as ak
import numpy
import talib
import datetime

def technical_analysis(code,period="daily",days=60):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days)
    #print(start_date,today)
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period=period, start_date=str(start_date).replace("-",""), end_date=str(today).replace("-",""), adjust="qfq")
    open = stock_zh_a_hist_df['开盘']
    high = stock_zh_a_hist_df['最高']
    low = stock_zh_a_hist_df['最低']
    close = stock_zh_a_hist_df['收盘']
    volume = stock_zh_a_hist_df['成交量']
    rsi = talib.RSI(close,timeperiod=14)
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    CDL2CROWS = talib.CDL2CROWS(open, high, low, close)
    CDL3BLACKCROWS = talib.CDL3BLACKCROWS(open, high, low, close)
    CDL3INSIDE =talib.CDL3INSIDE(open, high, low, close)
    CDL3LINESTRIKE = talib.CDL3LINESTRIKE(open, high, low, close)
    CDL3OUTSIDE = talib.CDL3OUTSIDE(open, high, low, close)
    CDL3STARSINSOUTH = talib.CDL3STARSINSOUTH(open, high, low, close)
    CDL3WHITESOLDIERS = talib.CDL3WHITESOLDIERS(open, high, low, close)
    CDLABANDONEDBABY = talib.CDLABANDONEDBABY(open, high, low, close)
    CDLADVANCEBLOCK = talib.CDLADVANCEBLOCK(open, high, low, close)
    CDLBELTHOLD = talib.CDLBELTHOLD(open, high, low, close)
    CDLBREAKAWAY = talib.CDLBREAKAWAY(open, high, low, close)
    CDLCLOSINGMARUBOZU = talib.CDLCLOSINGMARUBOZU(open, high, low, close)
    CDLCONCEALBABYSWALL = talib.CDLCONCEALBABYSWALL(open, high, low, close)
    CDLCOUNTERATTACK = talib.CDLCOUNTERATTACK(open, high, low, close)
    CDLDARKCLOUDCOVER = talib.CDLDARKCLOUDCOVER(open, high, low, close)
    CDLDOJI = talib.CDLDOJI(open, high, low, close)
    CDLDOJISTAR = talib.CDLDOJISTAR(open, high, low, close)
    CDLDRAGONFLYDOJI = talib.CDLDRAGONFLYDOJI(open, high, low, close)
    CDLENGULFING = talib.CDLENGULFING(open, high, low, close)
    CDLEVENINGDOJISTAR = talib.CDLEVENINGDOJISTAR(open, high, low, close)
    CDLEVENINGSTAR = talib.CDLEVENINGSTAR(open, high, low, close)
    CDLGAPSIDESIDEWHITE = talib.CDLGAPSIDESIDEWHITE(open, high, low, close)
    CDLGRAVESTONEDOJI = talib.CDLGRAVESTONEDOJI(open, high, low, close)
    CDLHAMMER = talib.CDLHAMMER(open, high, low, close)
    CDLHANGINGMAN = talib.CDLHANGINGMAN(open, high, low, close)
    CDLHARAMI = talib.CDLHARAMI(open, high, low, close)
    CDLHARAMICROSS = talib.CDLHARAMICROSS(open, high, low, close)
    CDLHIGHWAVE = talib.CDLHIGHWAVE(open, high, low, close)
    CDLHIKKAKE = talib.CDLHIKKAKE(open, high, low, close)
    CDLHIKKAKEMOD = talib.CDLHIKKAKEMOD(open, high, low, close)
    CDLHOMINGPIGEON = talib.CDLHOMINGPIGEON(open, high, low, close)
    CDLIDENTICAL3CROWS = talib.CDLIDENTICAL3CROWS(open, high, low, close)
    CDLINNECK = talib.CDLINNECK(open, high, low, close)
    CDLINVERTEDHAMMER = talib.CDLINVERTEDHAMMER(open, high, low, close)
    CDLKICKING = talib.CDLKICKING(open, high, low, close)
    CDLKICKINGBYLENGTH = talib.CDLKICKINGBYLENGTH(open, high, low, close)
    CDLLADDERBOTTOM = talib.CDLLADDERBOTTOM(open, high, low, close)
    CDLLONGLEGGEDDOJI = talib.CDLLONGLEGGEDDOJI(open, high, low, close)
    CDLLONGLINE = talib.CDLLONGLINE(open, high, low, close)
    CDLMARUBOZU = talib.CDLMARUBOZU(open, high, low, close)
    CDLMATCHINGLOW = talib.CDLMATCHINGLOW(open, high, low, close)
    CDLMATHOLD = talib.CDLMATHOLD(open, high, low, close)
    CDLMORNINGDOJISTAR = talib.CDLMORNINGDOJISTAR(open, high, low, close)
    CDLMORNINGSTAR = talib.CDLMORNINGSTAR(open, high, low, close)
    CDLONNECK = talib.CDLONNECK(open, high, low, close)
    CDLPIERCING = talib.CDLPIERCING(open, high, low, close)
    CDLRICKSHAWMAN = talib.CDLRICKSHAWMAN(open, high, low, close)
    CDLRISEFALL3METHODS = talib.CDLRISEFALL3METHODS(open, high, low, close)
    CDLSEPARATINGLINES = talib.CDLSEPARATINGLINES(open, high, low, close)
    CDLSHOOTINGSTAR = talib.CDLSHOOTINGSTAR(open, high, low, close)
    CDLSHORTLINE = talib.CDLSHORTLINE(open, high, low, close)
    CDLSPINNINGTOP = talib.CDLSPINNINGTOP(open, high, low, close)
    CDLSTALLEDPATTERN = talib.CDLSTALLEDPATTERN(open, high, low, close)
    CDLSTICKSANDWICH = talib.CDLSTICKSANDWICH(open, high, low, close)
    CDLTAKURI = talib.CDLTAKURI(open, high, low, close)
    CDLTASUKIGAP = talib.CDLTASUKIGAP(open, high, low, close)
    CDLTHRUSTING = talib.CDLTHRUSTING(open, high, low, close)
    CDLTRISTAR = talib.CDLTRISTAR(open, high, low, close)
    CDLUNIQUE3RIVER = talib.CDLUNIQUE3RIVER(open, high, low, close)
    CDLUPSIDEGAP2CROWS = talib.CDLUPSIDEGAP2CROWS(open, high, low, close)
    CDLXSIDEGAP3METHODS = talib.CDLXSIDEGAP3METHODS(open, high, low, close)
    all_patterns = [  CDL2CROWS,    CDL3BLACKCROWS,  CDL3INSIDE,     CDL3LINESTRIKE,  CDL3OUTSIDE,     CDL3STARSINSOUTH,  CDL3WHITESOLDIERS,
                      CDLABANDONEDBABY,  CDLADVANCEBLOCK,  CDLBELTHOLD,     CDLBREAKAWAY,    CDLCLOSINGMARUBOZU,  CDLCONCEALBABYSWALL,
                      CDLCOUNTERATTACK,  CDLDARKCLOUDCOVER,  CDLDOJI,     CDLDOJISTAR,  CDLDRAGONFLYDOJI,  CDLENGULFING,
                      CDLEVENINGDOJISTAR,  CDLEVENINGSTAR,  CDLGAPSIDESIDEWHITE,  CDLGRAVESTONEDOJI,  CDLHAMMER,     CDLHANGINGMAN,
                      CDLHARAMI,  CDLHARAMICROSS,  CDLHIGHWAVE,     CDLHIKKAKE,  CDLHIKKAKEMOD,  CDLHOMINGPIGEON,
                      CDLIDENTICAL3CROWS,  CDLINNECK,  CDLINVERTEDHAMMER,  CDLKICKING,  CDLKICKINGBYLENGTH,  CDLLADDERBOTTOM,
                      CDLLONGLEGGEDDOJI,  CDLLONGLINE,  CDLMARUBOZU,     CDLMATCHINGLOW,  CDLMATHOLD,     CDLMORNINGDOJISTAR,
                      CDLMORNINGSTAR,  CDLONNECK,  CDLPIERCING,     CDLRICKSHAWMAN,  CDLRISEFALL3METHODS,  CDLSEPARATINGLINES,
                      CDLSHOOTINGSTAR,  CDLSHORTLINE,  CDLSPINNINGTOP,     CDLSTALLEDPATTERN,  CDLSTICKSANDWICH,  CDLTAKURI,
                      CDLTHRUSTING,  CDLTRISTAR,  CDLUNIQUE3RIVER,  CDLUPSIDEGAP2CROWS,  CDLXSIDEGAP3METHODS]
    pattern_name = [  "CDL2CROWS","    CDL3BLACKCROWS","  CDL3INSIDE","     CDL3LINESTRIKE","  CDL3OUTSIDE","     CDL3STARSINSOUTH","  CDL3WHITESOLDIERS",
                    " CDLABANDONEDBABY","  CDLADVANCEBLOCK","  CDLBELTHOLD","     CDLBREAKAWAY","    CDLCLOSINGMARUBOZU","  CDLCONCEALBABYSWALL",
                      "CDLCOUNTERATTACK","  CDLDARKCLOUDCOVER","  CDLDOJI","     CDLDOJISTAR","  CDLDRAGONFLYDOJI","  CDLENGULFING",
                      "CDLEVENINGDOJISTAR","  CDLEVENINGSTAR","  CDLGAPSIDESIDEWHITE","  CDLGRAVESTONEDOJI","  CDLHAMMER","     CDLHANGINGMAN",
                     "CDLHARAMI","  CDLHARAMICROSS","  CDLHIGHWAVE","     CDLHIKKAKE","  CDLHIKKAKEMOD","  CDLHOMINGPIGEON",
                     "CDLIDENTICAL3CROWS","  CDLINNECK","  CDLINVERTEDHAMMER","  CDLKICKING","  CDLKICKINGBYLENGTH","  CDLLADDERBOTTOM",
                      "CDLLONGLEGGEDDOJI","  CDLLONGLINE","  CDLMARUBOZU","     CDLMATCHINGLOW","  CDLMATHOLD","     CDLMORNINGDOJISTAR",
                      "CDLMORNINGSTAR","  CDLONNECK","  CDLPIERCING","     CDLRICKSHAWMAN","  CDLRISEFALL3METHODS","  CDLSEPARATINGLINES",
                      "CDLSHOOTINGSTAR","  CDLSHORTLINE","  CDLSPINNINGTOP","     CDLSTALLEDPATTERN","  CDLSTICKSANDWICH","  CDLTAKURI",
                     "CDLTHRUSTING","  CDLTRISTAR","  CDLUNIQUE3RIVER","  CDLUPSIDEGAP2CROWS","  CDLXSIDEGAP3METHODS"]
    pattern = []
    for i in range(len(all_patterns)):
        if all_patterns[i][len(close)-1] != 0:
            pattern.append(pattern_name[i])

    upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=55, nbdevup=2, nbdevdn=2, matype=0)
    dic = {"当前价":close[len(close)-1],"rsi":rsi[len(close)-1],"macd":macd[len(close)-1],"macdsignal":macdsignal[len(close)-1],"macdhist":macdhist[len(close)-1],"布林轨道upperband":upperband[len(close)-1],"布林轨道middleband":middleband[len(close)-1],"布林轨道lowerband":lowerband[len(close)-1],"K线形态":pattern}
    return dic

