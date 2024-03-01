import plotly.graph_objs as go
import plotly
import plotly.express as px
import pandas as pd
import json 

def generate_plot_playlist(song_data, recommended_songs):
    energy = [song['energy'] for song in song_data]
    tempo = [song['tempo'] for song in song_data]
    acousticness = [song['acousticness'] for song in song_data]
    hover_text = [f'e: {round(song["energy"], 2)} t: {round(song["tempo"])} a: {round(song["acousticness"], 2)}' for song in song_data]
    custom_data = [(song['album_cover'], song['name'], song['artist'], song['energy'], song['tempo'], song['acousticness'], song['uri'], song['song_id']) for song in song_data]

    # Generate the scatter plot with Plotly
    fig = go.Figure(data=[go.Scatter3d(
        name='Playlist Songs',
        x=energy,
        y=tempo,
        z=acousticness,
        mode='markers',
        text=hover_text,  # This will be displayed on hover
        hoverinfo='text',
        customdata=custom_data,
        marker=dict(
            size=9,  # Adjust marker size
            opacity=1,
            color=tempo,  # Use energy for color scale
            colorscale=[  # Gradient color scale from burnt orange to light pink
                [0.0, 'rgb(204,85,0)'], 
                [1.0, 'rgb(255,182,193)']
            ]
        )
    )])

    rec_energy = [song['energy'] for song in recommended_songs]
    rec_tempo = [song['tempo'] for song in recommended_songs]
    rec_acousticness = [song['acousticness'] for song in recommended_songs]
    rec_hover_text = [f'e: {round(song["energy"], 2)} t: {round(song["tempo"])} a: {round(song["acousticness"], 2)}' for song in recommended_songs]
    rec_custom_data = [(song['album_cover'], song['name'], song['artist'], song['energy'], song['tempo'], song['acousticness'], song['uri'], song['song_id']) for song in recommended_songs]

        # Create a second scatter plot for the new data
    fig.add_trace(go.Scatter3d(
        name='Recommended Songs',
        x=rec_energy,
        y=rec_tempo,
        z=rec_acousticness,
        mode='markers',
        text=rec_hover_text,
        customdata=rec_custom_data,
        hoverinfo='text',
        marker=dict(
            size=9,  # You might choose a different size for differentiation
            opacity=0.8,  # Different opacity for the new data points
            color='#efcb68',  # Different color scale or single color for new data
        )
    ))

    # Setting the layout of the plot
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background in the plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the entire figure
        scene=dict(
            xaxis=dict(
                title='Energy',
                title_font=dict(color='#eeeeee'),
                gridcolor='rgba(230, 188, 205, 0.1)',
                linecolor='#eeeeee',
                backgroundcolor='rgba(0, 0, 0, 0)',
                showticklabels=True,
                tickfont=dict(color='#eeeeee'),
                zerolinecolor='#eeeeee',
                range=[0, 1],
            ),
            yaxis=dict(
                title='Tempo',
                title_font=dict(color='#eeeeee'),
                gridcolor='rgba(230, 188, 205, 0.1)',
                linecolor='#eeeeee',
                backgroundcolor='rgba(0, 0, 0, 0)',
                showticklabels=True,
                tickfont=dict(color='#eeeeee'),
                zerolinecolor='#eeeeee',
                range=[60, 160],
            ),
            zaxis=dict(
                title='Acousticness',
                title_font=dict(color='#eeeeee'),
                gridcolor='rgba(230, 188, 205, 0.1)',
                linecolor='#eeeeee',
                backgroundcolor='rgba(0, 0, 0, 0)',
                showticklabels=True,
                tickfont=dict(color='#eeeeee'),
                zerolinecolor='#eeeeee',
                range=[0, 1],
            ),
            bgcolor='rgba(0,0,0,0)',
            camera=dict(
                eye=dict(x=1.6, y=1.6, z=1.6)
            )
        ),
        legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(
                family="Poppins, sans-serif",
                size=16,
                color="#eeeeee"
            ),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#eeeeee'
        )
    )


    # Convert the figure to JSON for easy rendering in JavaScript
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def plot_profiles(profiles_data):
    # Data preparation
    x = [profile.x for profile in profiles_data]
    y = [profile.y for profile in profiles_data]
    names = [profile.name for profile in profiles_data]
    df = pd.DataFrame({'x': x, 'y': y, 'name': names})

    # Creating the scatter plot
    fig = px.scatter(df, x='x', y='y')

    fig.update_traces(marker=dict(size=18))

    # Customizing layout
    fig.update_layout(
        title='Explore',
        title_font_size=20,
        title_x=0.5,  # Center title
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        xaxis=dict(
            range=[-1, 1],  # Custom x-axis range for zoom effect
            showgrid=False,  # Remove gridlines
            title_font=dict(size=18),
            zeroline=False  # Remove the zero line
        ),
        yaxis=dict(
            range=[-1, 1],  # Custom y-axis range for zoom effect
            showgrid=False,  # Remove gridlines
            title_font=dict(size=18),
            zeroline=False  # Remove the zero line
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        font=dict(family='Poppins', size=12, color='#7f7f7f'),  # Font settings
        showlegend=False  # Remove legend
    )

    # Remove color bar
    fig.update_traces(marker=dict(color='rgb(204,85,0)'))  # Set a single color for all points

    # Convert to JSON
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return plot_json