from sanic import Sanic
from app.routes.hello_routes import HelloRoute
from app.config import get_config
# from app.conn import PoolCreator, Base
from app.session import SessionCreator, Base


app = Sanic("Hide", config=get_config())
app.add_route(HelloRoute.get, '/', methods=["GET"])



@app.before_server_start
async def setup_db(app, _):
	session_creator = SessionCreator(app.config)

	async with session_creator.engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

	# async with session_creator.get_session() as session:
	# 	pass

	# pool_creator = PoolCreator(app.config)
	# app.ctx.pool = await pool_creator.create_pool()

	# engine = pool_creator.create_engine()
	# async with engine.begin() as conn:
	# 	await conn.run_sync(Base.metadata.drop_all)
	# 	await conn.run_sync(Base.metadata.create_all)


@app.on_request
async def example(request):
	# request.ctx.conn = request.app.ctx.session_creator.get_session()
	print("I execute before the handler.")


@app.on_response
async def example(request, response):
	print("I execute after the handler.")
