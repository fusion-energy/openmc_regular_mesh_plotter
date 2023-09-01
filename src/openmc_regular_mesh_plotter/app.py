import openmc
import streamlit as st
from matplotlib.colors import LogNorm
import openmc_regular_mesh_plotter as rmp
import matplotlib.pyplot as plt


def save_uploadedfile(uploadedfile):
    with open(uploadedfile.name, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success(f"Saved File to {uploadedfile.name}")


def header():
    """This section writes out the page header common to all tabs"""

    st.set_page_config(
        page_title="OpenMC Regular Mesh Plotter",
        page_icon="⚛",
        layout="wide",
    )

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {
                    visibility: hidden;
                    }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.write(
        """
            # OpenMC Regular Mesh Plotter

            ### ⚛ A plotting user interface for regular meshes.

            🐍 Run this app locally with Python ```pip install openmc_regular_mesh_plotter``` then run with ```openmc_regular_mesh_plotter```

            ⚙ Produce MatPlotLib plots in batch with the 🐍 [Python API](https://github.com/fusion-energy/openmc_regular_mesh_plotter/tree/master/examples)

            💾 Raise a feature request, report and issue or make a contribution on [GitHub](https://github.com/fusion-energy/openmc_regular_mesh_plotter)

            📧 Email feedback to mail@jshimwell.com

            🔗 This package forms part of a more [comprehensive openmc plot](https://github.com/fusion-energy/openmc_plot) package where geometry, tallies, slices, etc can be plotted and is hosted on [xsplot.com](https://www.xsplot.com/) .
        """
    )

    st.write("<br>", unsafe_allow_html=True)


def main():
    st.write(
        """
            👉 Carry out an OpenMC simulation to generate a ```statepoint.h5``` file.

        """
        # Not got a h5 file handy, right mouse 🖱️ click and save these links
        # [ example 1 ](https://fusion-energy.github.io/openmc_regular_mesh_plotter/examples/csg_tokamak/geometry.xml),
        # [ example 2 ](https://fusion-energy.github.io/openmc_regular_mesh_plotter/examples/csg_cylinder_box/geometry.xml)
    )

    statepoint_file = st.file_uploader("Select your statepoint h5 file", type=["h5"])

    if statepoint_file is None:
        new_title = '<center><p style="font-family:sans-serif; color:Red; font-size: 30px;">Select your statepoint h5 file</p></center>'
        st.markdown(new_title, unsafe_allow_html=True)

    else:
        save_uploadedfile(statepoint_file)
        statepoint = openmc.StatePoint(statepoint_file.name)

        tally_description = rmp.get_regularmesh_tallies_and_scores(statepoint)
        tally_description_str = [
            f"ID={td['id']} score={td['score']} name={td['name']}"
            for td in tally_description
        ]

        tally_description_to_plot = st.sidebar.selectbox(
            label="Tally to plot", options=tally_description_str, index=0
        )
        tally_id_to_plot = tally_description_to_plot.split(" ")[0][3:]
        tally_score_to_plot = tally_description_to_plot.split(" ")[1][6:]

        view_direction = st.sidebar.selectbox(
            label="view direction",
            options=("xz", "yz", "xy"),
            index=0,
            key="axis",
            help="",
        )

        tally_or_std = st.sidebar.radio(
            "Tally mean or std dev", options=["mean", "std_dev"]
        )

        volume_normalization = st.sidebar.radio(
            "Divide value by mesh voxel volume", options=[True, False]
        )

        value_multiple = st.sidebar.number_input(
            "Multiplier value",
            value=1.0,
            help="Input a number that will be used to scale the mesh values. For example a input of 2 would double all the values.",
        )

        my_tally = statepoint.get_tally(id=int(tally_id_to_plot))
        score = my_tally.get_values(
            scores=[tally_score_to_plot], value=tally_or_std
        ).flatten()
        mesh = my_tally.find_filter(filter_type=openmc.MeshFilter).mesh
        extent = mesh.get_mpl_plot_extent(view_direction=view_direction)

        slice_index = st.sidebar.slider(
            label="slice index",
            min_value=1,
            value=1,
            max_value=mesh.get_number_of_slices(view_direction=view_direction),
        )

        if tally_or_std == "mean":
            cbar_label = tally_score_to_plot
        else:  # 'std dev'
            cbar_label = f"standard deviation {tally_score_to_plot}"

        title = st.sidebar.text_input(
            "Colorbar title",
            help="Optionally set your own colorbar label for the plot",
            value=cbar_label,
        )

        log_lin_scale = st.sidebar.radio("Scale", options=["log", "linear"])
        if log_lin_scale == "linear":
            norm = None
        else:
            norm = LogNorm()

        xlabel, ylabel = mesh.get_axis_labels(view_direction=view_direction)

        extent = None  # not yet figured out
        theta, r, values = mesh.slice_of_data(
            dataset=score,  # ,
            view_direction=view_direction,
            slice_index=slice_index,
            volume_normalization=volume_normalization,
        )
        values = values * value_multiple
        fig, axes = plt.subplots(subplot_kw=dict(projection="polar"))
        im = axes.contourf(
            theta, r, values, extent=extent, norm=norm
        )  # , locator=ticker.LogLocator())

        if contour_levels_str:
            axes.contour(
                theta,
                r,
                values,
                levels=contour_levels,
                colors="darkgrey",
                linewidths=1,
                extent=extent,
            )

        plt.colorbar(im, label=title, ax=axes)

        plt.savefig("openmc_plot_regularmesh_image.png")
        with open("openmc_plot_regularmesh_image.png", "rb") as file:
            st.download_button(
                label="Download image",
                data=file,
                file_name="openmc_plot_regularmesh_image.png",
                mime="image/png",
            )
        st.pyplot(plt)


if __name__ == "__main__":
    header()
    main()
