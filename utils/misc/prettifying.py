

async def money_format(value):
    pretty_value = '{0:,.2f}'.format(value).replace(',', ' ').replace('.', ',')

    return pretty_value

async def grades_format(value):
    pretty_value = '{0:,.0f}'.format(value).replace(',', ' ').replace('.', ',')

    return pretty_value
