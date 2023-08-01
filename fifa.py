from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import Screen, MDScreen
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import unidecode
import os
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FigureCanvas

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MainScreen(Screen):
    pass

df = pd.read_csv("D:\\USUARIO\\Documents\\Datasets\\fifa22\\players_22.csv",low_memory=False)

class FifaApp(MDApp):
    #player personal info
    init_default_player_name = df.iloc[0]['short_name']
    init_default_player_position = df.iloc[0]['player_positions']
    init_default_player_age = str(df.iloc[0]['age'])
    init_default_player_nationality_name = df.iloc[0]['nationality_name']
    #flags
    flag_file_path = "D:\\USUARIO\\Documents\\pipi_files\\fifa\\src\\countries\\"
    init_default_player_nationFlag_url = df.iloc[0]['nation_flag_url']
    flag_filename = os.path.splitext(os.path.basename(init_default_player_nationFlag_url))[0]
    init_flag_url = flag_file_path+flag_filename
    #player characteristics
    init_default_player_overall = 'GER\n'+str(df.iloc[0]['overall'])
    init_default_player_passing = str(df.iloc[0]['passing'])
    init_default_player_defending = str(df.iloc[0]['defending'])
    init_default_player_shooting = str(df.iloc[0]['shooting'])
    init_default_player_physic = str(df.iloc[0]['physic'])
    init_default_player_dribbling = str(df.iloc[0]['dribbling'])
    init_default_player_pace = str(df.iloc[0]['pace'])
    #rating skill moves and weak foot
    init_default_player_skillMoves = df.iloc[0]['skill_moves']
    init_default_player_weakFoot = df.iloc[0]['weak_foot']

    # PLAYER SKILLS AVERAGES
    numbers_pac = [df.iloc[0]['movement_sprint_speed'], df.iloc[0]['movement_acceleration']]
    init_average_pac = sum(numbers_pac) / len(numbers_pac)
    numbers_sho = [
        df.iloc[0]['attacking_finishing'], df.iloc[0]['mentality_positioning'], df.iloc[0]['power_shot_power'],
        df.iloc[0]['power_long_shots'], df.iloc[0]['mentality_penalties'], df.iloc[0]['attacking_volleys']
    ]
    init_average_sho = sum(numbers_sho) / len(numbers_sho)
    numbers_pas = [
        df.iloc[0]['mentality_vision'], df.iloc[0]['attacking_crossing'], df.iloc[0]['skill_fk_accuracy'],
        df.iloc[0]['skill_long_passing'], df.iloc[0]['attacking_short_passing'], df.iloc[0]['skill_curve']
    ]
    init_average_pas = sum(numbers_pas) / len(numbers_pas)
    numbers_dri = [
        df.iloc[0]['movement_agility'], df.iloc[0]['movement_balance'], df.iloc[0]['movement_reactions'],
        df.iloc[0]['mentality_composure'], df.iloc[0]['skill_ball_control'], df.iloc[0]['dribbling']
    ]
    init_average_dri = sum(numbers_dri) / len(numbers_dri)
    numbers_def = [
        df.iloc[0]['mentality_interceptions'], df.iloc[0]['attacking_heading_accuracy'],
        df.iloc[0]['defending_marking_awareness'], df.iloc[0]['defending_standing_tackle'],
        df.iloc[0]['defending_sliding_tackle']
    ]
    init_average_def = sum(numbers_def) / len(numbers_def)
    numbers_phy = [
        df.iloc[0]['power_jumping'], df.iloc[0]['power_stamina'], df.iloc[0]['power_strength'],
        df.iloc[0]['mentality_aggression']
    ]
    init_average_phy = sum(numbers_phy) / len(numbers_phy)
    # PLAYER SKILL AVERAGES
    # init chart step
    chart = None
    def create_chart(self, values=None):
        self.root.ids.chart_box_layout.orientation = 'vertical'
        # Data from the variables
        labels = ['PAS', 'SHO', 'PAC', 'PHY', 'DEF', 'DRI']
        if values is None:
            #values = [int(round(float(self.init_default_player_skillMoves))),int(round(float(self.init_default_player_shooting))),int(round(float(self.init_default_player_pace))),int(round(float(self.init_default_player_physic))),int(round(float(self.init_default_player_defending))),int(round(float(self.init_default_player_dribbling))),
            values = [int(round(float(self.init_average_pas))),
                      int(round(float(self.init_average_sho))),
                      int(round(float(self.init_average_pac))),
                      int(round(float(self.init_average_phy))),
                      int(round(float(self.init_average_def))),
                      int(round(float(self.init_average_dri))),
            ]
        else:
            pass
        # to implement font-family in the future
        #matplotlib.rcParams['font.family'] = 'sans-serif'
        #matplotlib.rcParams['font.sans-serif'] = 'Roboto'
        # to implement font-family in the future
        # Number of variables plotting.
        num_vars = len(labels)
        # Split the circle into even parts and save the angles so we know where to put each axis.
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        # The plot is a circle, so we need to "complete the loop" and append the start value to the end.
        values += values[:1]
        angles += angles[:1]
        # Create figure and polar axis
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        # Set the background color of the figure to transparent
        fig.set_facecolor('none')
        ax.set_facecolor('none')
        # draw the chart lines
        filled_area = ax.plot(angles, values, color='red', linewidth=1)
        # Set the edgecolor of the filled area to white
        #for area in filled_area:
            #area.set_color('white')
        # Fill the area inside the chart
        ax.fill(angles, values, color='red', alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, color='white',fontname='Arial',weight='bold')
        # Removes value labels from radial grids
        ax.set_yticklabels([])
        # Set the color of the radial grid lines to white
        ax.grid(color='white')
        # Removes the inner circular lines from the graph
        ax.yaxis.grid(False)
        # Set the color of the circular grid lines to white
        for _, spine in ax.spines.items():
            spine.set_edgecolor('white')
        # Create the FigureCanvasKivyAgg object to display the graph in Kivy
        canvas = FigureCanvas(fig)
        # If a previous chart already exists, remove it
        if self.chart is not None:
            self.root.ids.chart_box_layout.remove_widget(self.chart)
        # Create the FigureCanvasKivyAgg object to display the new graphic in Kivy
        #canvas = FigureCanvas(fig) # old wrong way
        self.root.ids.chart_box_layout.add_widget(canvas)
        # Stores the new chart reference for future updates when searching for players
        self.chart = canvas

    # RATING SYSTEM DOWNSIDE
    # create the star rating update for skill moves
    def update_skill_moves_icon(self):
        for i in range(5, 0, -1):
            icon_id = f'skill_icon_star_{i}'
            if i > self.init_default_player_skillMoves:
                self.root.ids[icon_id].icon = 'star-outline'
            else:
                self.root.ids[icon_id].icon = 'star'
    # create the star rating update for weak foot
    def update_weak_foot_icon(self):
        for i in range(5, 0, -1):
            icon_id = f'weakFoot_icon_star_{i}'
            if i > self.init_default_player_weakFoot:
                self.root.ids[icon_id].icon = 'star-outline'
            else:
                self.root.ids[icon_id].icon = 'star'
    # RATING SYSTEM UPSIDE
    #create the attack/defense system: high/medium/low
    init_default_att_def_rating = df.iloc[0]['work_rate']
    split_att_def_rating = init_default_att_def_rating.split("/")
    init_default_player_attackRating = split_att_def_rating[0]
    init_default_player_defenseRating = split_att_def_rating[1]
    # create the attack/defense system: high/medium/low
    def build(self):
        self.update_skill_moves_icon()
        self.update_weak_foot_icon()
        self.create_chart()
    def select_player(self, instance, touch):
        if instance.collide_point(*touch.pos):  # Checks if the tap occurred on the widget
            player_name = instance.text  # Gets the name of the selected player
            # Query the dataframe to get the specific player information
            player_info = df[df['long_name'] == player_name]
            # update player personal info
            pl_age = str(player_info['age'].values[0])
            pl_pos = player_info['player_positions'].values[0]
            pl_nation = player_info['nationality_name'].values[0]
            #get flag update
            nationFlag_name = player_info['nation_flag_url'].values[0]
            get_flag_fileName = os.path.splitext(os.path.basename(nationFlag_name))[0]
            pl_flag = "D:\\USUARIO\\Documents\\pipi_files\\fifa\\src\\countries\\"+get_flag_fileName+".png"
            # player characteristics
            pl_overall = 'GER\n'+str(player_info['overall'].values[0])
            cols_to_fill = ['shooting', 'pace', 'physic', 'defending', 'dribbling']
            player_info[cols_to_fill] = player_info[cols_to_fill].fillna(0)
            pl_passing = str(player_info['passing'].values[0])
            pl_defending = str(player_info['defending'].values[0])
            pl_shooting = str(player_info['shooting'].values[0])
            pl_physic = str(player_info['physic'].values[0])
            pl_dribbling = str(player_info['dribbling'].values[0])

            pl_pace = str(player_info['pace'].values[0])
            pl_skillMoves = player_info['skill_moves'].values[0]
            pl_weakFoot = player_info['weak_foot'].values[0]
            # player characteristics

            #update the attack/defense system: high/medium/low
            att_def = player_info['work_rate'].values[0]
            split_att_def = att_def.split("/")
            pl_attackingRating = split_att_def[0]
            pl_defenseRating = split_att_def[1]

            # update the labels
            self.root.ids.player_name_label_id.text = player_name
            self.root.ids.player_age_label_id.text = 'Idade: '+pl_age
            self.root.ids.player_pos_label_id.text = 'Pos: ' + pl_pos
            self.root.ids.player_flag_image_id.source = pl_flag
            self.root.ids.player_nationalityName_label_id.text = pl_nation
            self.root.ids.player_overall_label_id.text = pl_overall
            self.root.ids.player_defending_label_id.text = pl_defending
            self.root.ids.player_physic_label_id.text = pl_physic
            self.root.ids.player_dribbling_label_id.text = pl_dribbling
            self.root.ids.player_passing_label_id.text = pl_passing
            self.root.ids.player_shooting_label_id.text = pl_shooting
            self.root.ids.player_pace_label_id.text = pl_pace

            # star rating update for skill
            for i in range(5, 0, -1):
                icon_id = f'skill_icon_star_{i}'
                if i > pl_skillMoves:
                    self.root.ids[icon_id].icon = 'star-outline'
                else:
                    self.root.ids[icon_id].icon = 'star'
            # star rating update for skill
            # star rating update for weakFoot
            for i in range(5, 0, -1):
                icon_id = f'weakFoot_icon_star_{i}'
                if i > pl_weakFoot:
                    self.root.ids[icon_id].icon = 'star-outline'
                else:
                    self.root.ids[icon_id].icon = 'star'

            self.root.ids.player_attackRating_label_id.text = pl_attackingRating
            self.root.ids.player_defenseRating_label_id.text = pl_defenseRating
            # star rating update for weakFoot

            # UPDATE THE AVERAGE
            update_numbers_pac = [player_info.iloc[0]['movement_sprint_speed'], player_info.iloc[0]['movement_acceleration']]
            player_average_pac = sum(update_numbers_pac) / len(update_numbers_pac)
            numbers_sho = [
                player_info.iloc[0]['attacking_finishing'], player_info.iloc[0]['mentality_positioning'], player_info.iloc[0]['power_shot_power'],
                player_info.iloc[0]['power_long_shots'], player_info.iloc[0]['mentality_penalties'], player_info.iloc[0]['attacking_volleys']
            ]
            player_average_sho = sum(numbers_sho) / len(numbers_sho)
            update_numbers_pas = [
                player_info.iloc[0]['mentality_vision'], player_info.iloc[0]['attacking_crossing'], player_info.iloc[0]['skill_fk_accuracy'],
                player_info.iloc[0]['skill_long_passing'], player_info.iloc[0]['attacking_short_passing'], player_info.iloc[0]['skill_curve']
            ]
            player_average_pas = sum(update_numbers_pas) / len(update_numbers_pas)
            update_numbers_dri = [
                player_info.iloc[0]['movement_agility'], player_info.iloc[0]['movement_balance'], player_info.iloc[0]['movement_reactions'],
                player_info.iloc[0]['mentality_composure'], player_info.iloc[0]['skill_ball_control'], player_info.iloc[0]['dribbling']
            ]
            player_average_dri = sum(update_numbers_dri) / len(update_numbers_dri)
            update_numbers_def = [
                player_info.iloc[0]['mentality_interceptions'], player_info.iloc[0]['attacking_heading_accuracy'],
                player_info.iloc[0]['defending_marking_awareness'], player_info.iloc[0]['defending_standing_tackle'],
                player_info.iloc[0]['defending_sliding_tackle']
            ]
            player_average_def = sum(update_numbers_def) / len(update_numbers_def)
            update_numbers_phy = [
                player_info.iloc[0]['power_jumping'], player_info.iloc[0]['power_stamina'], player_info.iloc[0]['power_strength'],
                player_info.iloc[0]['mentality_aggression']
            ]
            player_average_phy = sum(update_numbers_phy) / len(update_numbers_phy)
            # UPDATE THE AVERAGE
            # update the chart values
            values = [
            int(round(float(player_average_pas))),
            int(round(float(player_average_sho))),
            int(round(float(player_average_pac))),
            int(round(float(player_average_phy))),
            int(round(float(player_average_def))),
            int(round(float(player_average_dri))),
                      ]
            self.create_chart(values)
            # update the chart values

    # search the player based on the user input
    def search_player(self):
        search_text = unidecode.unidecode(self.root.ids.id_search_field_player.text.lower())
        df['long_name_normalized'] = df['long_name'].apply(lambda x: unidecode.unidecode(x.lower()))
        results = df[df['long_name_normalized'].str.contains(search_text, case=False)]
        scroll_layout = self.root.ids.scroll_layout  # Gets the reference to the GridLayout inside the ScrollView
        scroll_layout.clear_widgets()  # Remove existing widgets

        for index, player in results.iterrows():  # Iterates over the found players
            player_name = player['long_name']  # retrieve the name of player
            label = MDLabel(text=player_name, halign='center', font_size='16sp',theme_text_color="Custom",text_color=(1, 1, 1, 1),adaptive_height=True)  # add a new label for player
            label.bind(on_touch_up=self.select_player)
            scroll_layout.add_widget(label)  # add the MDLabel on GridLayout
        self.root.ids.scroll_view.scroll_y = 1
    # search the player based on the user input

if __name__ == '__main__':
    FifaApp().run()