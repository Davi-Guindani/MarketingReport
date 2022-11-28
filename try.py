from Info.Infos import Info,InsightInfo, BasicInfo, RangedInsightInfo

lista = []
for field in Info.user_fields:
    lista.append(BasicInfo(field).set_info())

for insight in Info.user_insights:
    if insight in Info.not_ranged_insights:
        lista.append(InsightInfo(insight).set_info())
    if insight in Info.ranged_insights:
        lista.append(RangedInsightInfo(insight).set_info())

print(lista)