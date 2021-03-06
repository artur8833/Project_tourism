from flask import Flask, render_template
from flask_admin import Admin
from flask_login import LoginManager
from webapp.admin import RouteImageView, form, CoordinateModelView, DetailModelView, VisualModelView
from webapp.extensions import db, migrate
from webapp.model import Route, Coordinate, Detail, Visual
from webapp.user.model import User
from webapp.user.views import blueprint as user_blueprint
from flask import Flask, render_template, request, flash, redirect
from webapp.model import Route, Coordinate, Detail, Visual, Coordinateformap
from webapp.extensions import db, migrate
from webapp.admin import RouteImageView, CoordinateModelView, DetailModelView, VisualModelView, CoordinateformapModelView
from flask_admin import Admin, form
from webapp.weather import weather_by_city
import folium
from folium import IFrame
import base64
import json
import os
from pathlib import Path


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config["FLASK_ADMIN_SWATCH"] = 'cerulean'
    app.config['SECRET_KEY'] = '123456'
    app.register_blueprint(user_blueprint)
    register_extensions(app)
    admin = Admin(app, name='map_rout', template_mode='bootstrap3')
    register_admin_views(admin)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader

    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')

    def index():
        map_rout = Route.query.all()
        weather = weather_by_city("Sochi, Russia")
        return render_template("index.html", map_rout=map_rout, thumbnail=form.thumbgen_filename, weather=weather)

    @app.route('/load/<int:pk>', methods=['GET', 'POST'])

    def upload_file(pk):
        route = Route.query.filter_by(id=pk).first()

        if request.method == 'POST':
            if 'file' not in request.files:
                flash('Не могу прочитать файл')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('Нет выбранного файла')
                return redirect(request.url)
            if file:
                read_file = file.read().decode('utf-8')
                coordinate_for_file = json.loads(read_file)
                route = next(iter(coordinate_for_file.get("features", [])), None)
                route_properties = route.get("properties", {})
                route_title = route_properties.get("name")
                route_coordinates = route.get('geometry', {}).get('coordinates', [])

                for position, coordinates in enumerate(route_coordinates):
                    coordinates = Coordinate(latitude=coordinates[1],
                                            longitude=coordinates[0],
                                            route_id=route.id,
                                            order=position)
                    db.session.add(coordinates)
                db.session.commit()
        return render_template("download.html")

    @app.route('/<int:pk>')
    
    def detail(pk):
        coordinates = Coordinate.query.filter_by(route_id=pk).all()
        coordinates_for_rout = Coordinateformap.query.filter_by(route_id=pk).all()
        maps_routes = Route.query.filter_by(id=pk).first()
        detail_routes = Detail.query.filter_by(id=pk).first()
        loc = [(c.latitude, c.longitude) for c in coordinates]

        folium_map = folium.Map(location=loc[1],
                                zoom_start=13,
                                width=1000,
                                height=600,
                                top=80)

        polyline_options = {
            'color': 'blue',
            'weight': 5,
            'opacity': 0.8,
            }

        folium.PolyLine(loc, **polyline_options).add_to(folium_map)

        base_dir = Path(__file__).resolve().parent
        for coordinate_map in coordinates_for_rout:
            image_file = coordinate_map.image_for_map
            image_path = os.path.join(base_dir, 'static', 'media', image_file)
            title = f'{coordinate_map.title}'
            picture = base64.b64encode(open(image_path, 'rb').read()).decode()
            html = f'{title}<img src="data:image/JPG;base64,{picture}">'
            iframe = IFrame(html, width=632 + 20, height=420 + 20)
            popup = folium.Popup(iframe, max_width=1000)

            folium.Marker(location=(coordinate_map.longitude_for_image, coordinate_map.latitude_for_image),
                          popup=popup,
                          icon=folium.Icon(icon='info-sign', color="blue"),
                          draggable=False).add_to(folium_map)

        folium.Marker(location=loc[0],
                      popup="Начало маршрута",
                      icon=folium.Icon(icon='info-sign', color="red"),
                      draggable=False).add_to(folium_map)


        return render_template("detail.html", maps_routes=maps_routes, detail_routes=detail_routes,
                               folium_map=folium_map._repr_html_())
                               
    return app


def register_admin_views(admin):
    admin.add_view(RouteImageView(Route, db.session))
    admin.add_view(CoordinateModelView(Coordinate, db.session))
    admin.add_view(DetailModelView(Detail, db.session))
    admin.add_view(VisualModelView(Visual, db.session))
    admin.add_view(CoordinateformapModelView(Coordinateformap, db.session))


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    return None
