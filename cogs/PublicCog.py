from discord.ext.commands import Cog
from discord import (
    ApplicationContext,
    SlashCommandGroup,
    SlashCommandOptionType,
    Option,
)
from client import LunaClient
from models.user import User
from sqlalchemy import text


class Public(Cog):
    group = SlashCommandGroup(
        "public", "List of public commands", guild_ids=[957867801119449109]
    )

    def __init__(self, client: LunaClient):
        self.client = client

    @group.command(
        name="setup",
        description="Allows you to setup your profile and choose your starter stats",
    )
    async def setup(self, ctx: ApplicationContext):
        transaction = self.client.session()

        result = transaction.execute(
            text("SELECT EXISTS(SELECT 1 FROM public.user WHERE id=:id)").bindparams(
                id=ctx.author.id
            )
        ).first()

        if result[0]:
            return await ctx.respond("An account already exists for your discord user.")

        new_user = User(id=ctx.author.id)

        transaction.add(new_user)

        transaction.commit()

        await ctx.respond("Created a user for you!")

    @group.command(name="profile", description="View yours or someone elses profile")
    async def profile(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user, "Who do you want to view", required=False
        ),  # type: ignore
    ):
        user = user or ctx.author

        profile = self.client.session().query(User).filter_by(id=user.id).first()

        if profile is None:
            return await ctx.respond(f"There was no profile for {user.name}")

        await ctx.respond(f"`{profile}`")


def setup(client: LunaClient):
    client.add_cog(Public(client))
