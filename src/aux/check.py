def is_spam(ctx):
    return (ctx.message.channel.id == 418502930602131457) | ctx.message.channel.is_nsfw()
