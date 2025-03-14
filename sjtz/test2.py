
with open("try/industry_report.md", "w", encoding="utf-8") as file:
        file.write(industry_report)
    with open("try/sentiment_report.md", "w", encoding="utf-8") as file:
        file.write(sentiment_report)
    with open("try/technique_report.md", "w", encoding="utf-8") as file:
        file.write(technique_report)


with open("try/section1.md", "w", encoding="utf-8") as file:
        file.write(section1)

    with open("try/section2.md", "w", encoding="utf-8") as file:
        file.write(section2)
        with open("try/section3.md", "w", encoding="utf-8") as file:
        file.write(section3)  
        with open("try/memory_report.md", "w", encoding="utf-8") as file:
            file.write(memory_report)


with open("try/summary.md", "w", encoding="utf-8") as file:
        file.write(summary)








with open("try/industry_report.md", "w", encoding="utf-8") as file:
        file.write(industry_report)
    with open("try/sentiment_report.md", "w", encoding="utf-8") as file:
        file.write(sentiment_report)
    with open("try/technique_report.md", "w", encoding="utf-8") as file:
        file.write(technique_report)


    with open("try/reviewer_report.md", "w", encoding="utf-8") as file:
        file.write(reviewer_report)

    prom = f"""
    请基于审阅者提供的意见：'{reviewer_report}'，帮我修改一下下面的金融分析报告。
    要点：务必保证原报告的完整性和准确性，除了审阅者提供意见的地方，其余部分保持原样。
    金融分析报告: '{draft}'"""
    revise_report = call_model(content= "你是一位专业的金融分析报告编辑,你的目标是根据审阅者的意见对初稿进行修订。你被审阅者委以重任，负责修订一份由非专业人士撰写的初稿。如果你决定遵循审阅者的意见，请根据初稿进行修改，并确保解决他们提出的所有问题，并根据内容为每个章节重新拟制合适的标题。"+prom+"请以markdown格式输出。")

    with open("try/revise_report.md", "w", encoding="utf-8") as file:
        file.write(revise_report)




    with open("try/draft1.md", "w", encoding="utf-8") as file:
            file.write(draft1)

    with open("try/draft2.md", "w", encoding="utf-8") as file:
            file.write(draft2)
    
    with open("try/draft3.md", "w", encoding="utf-8") as file:
            file.write(draft3)
    

    with open("try/memory_report.md", "w", encoding="utf-8") as file:
            file.write(memory_report)


with open("try/writer_report.md", "w", encoding="utf-8") as file:
            file.write(draft4)
        

with open("try/industry_report.md", "r", encoding="utf-8") as file:
        industry_report = file.read()
    with open("try/sentiment_report.md", "r", encoding="utf-8") as file:
        sentiment_report = file.read()
    with open("try/technique_report.md", "r", encoding="utf-8") as file:
        technique_report = file.read()


  with open("try/draft3.md", "r", encoding="utf-8") as file:
            draft3 = file.read()
    with open("try/memory_report.md", "r", encoding="utf-8") as file:
            memory_report = file.read()
    
    with open("try/draft4.md", "r", encoding="utf-8") as file:
            draft4 = file.read()

    reviewer_report = call_model(content= "你是一名专业的金融分析报告审稿人。你被要求审阅一份由非专业人士撰写的初稿，请提供适当的修订意见。初稿如下："+draft)
    with open("try/reviewer_report.md", "w", encoding="utf-8") as file:
        file.write(reviewer_report)

    prom = f"""你是一位专业的金融分析报告写作者,你的目标是根据审阅者的意见对金融分析报告进行修订。请在初稿基础上进行修改，并确保解决审阅者提出的所有问题，最终根据内容为每个章节重新拟制合适的标题。
    审阅者提供的意见：'{reviewer_report}'
    金融分析报告: '{draft}'
    要点：务必保证原报告结构的完整性，字数不得低于原报告，除了审阅者提供意见的地方，报告其余部分不得修改。
    请使用Markdown格式回答，但不要用任何代码块（如 ```）包裹内容。
    返回修改后的金融分析报告全文，字数不得低于原报告的80%。
    """
    revise_report = call_model(content= prom)

 with open("try/draft4.md", "w", encoding="utf-8") as file:
            file.write(draft4)