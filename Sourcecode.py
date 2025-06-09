import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Constants and data
feed_flow = 100  # kmol/hr

boiling_points = {
    'n-hexane': 69,
    'n-octane': 126,
    'n-decane': 174,
    'benzene': 80,
    'toluene': 111
}

molecular_weights = {
    'n-hexane': 86.18,
    'n-octane': 114.23,
    'n-decane': 142.29,
    'benzene': 78.11,
    'toluene': 92.14
}

carbon_numbers = {
    'n-hexane': 6,
    'n-octane': 8,
    'n-decane': 10,
    'benzene': 6,
    'toluene': 7
}

cuts = {
    'Naphtha': (30, 100),
    'Kerosene': (100, 150),
    'Diesel': (150, 200),
    'Residue': (200, 400)
}

heat_of_vaporization = {
    'n-hexane': 33000,
    'n-octane': 35000,
    'n-decane': 36000,
    'benzene': 33000,
    'toluene': 35000
}

heat_capacity = {
    'n-hexane': 180,
    'n-octane': 220,
    'n-decane': 270,
    'benzene': 150,
    'toluene': 190
}

def calculate_products(feed_comp):
    products_mol = {cut: 0 for cut in cuts}
    products_mass = {cut: 0 for cut in cuts}
    products_bp_sum = {cut: 0 for cut in cuts}
    products_mol_sum = {cut: 0 for cut in cuts}
    products_cnum_sum = {cut: 0 for cut in cuts}

    for comp, frac in feed_comp.items():
        mol_flow = frac * feed_flow
        mw = molecular_weights[comp]
        mass_flow = mol_flow * mw
        bp = boiling_points[comp]
        c_num = carbon_numbers[comp]

        assigned = False
        for cut, (bp_low, bp_high) in cuts.items():
            if bp_low <= bp < bp_high:
                products_mol[cut] += mol_flow
                products_mass[cut] += mass_flow
                products_bp_sum[cut] += bp * mol_flow
                products_mol_sum[cut] += mol_flow
                products_cnum_sum[cut] += c_num * mol_flow
                assigned = True
                break
        if not assigned:
            # Residue fallback
            products_mol['Residue'] += mol_flow
            products_mass['Residue'] += mass_flow
            products_bp_sum['Residue'] += bp * mol_flow
            products_mol_sum['Residue'] += mol_flow
            products_cnum_sum['Residue'] += c_num * mol_flow

    return products_mol, products_mass, products_bp_sum, products_mol_sum, products_cnum_sum

def estimate_heat_duty(feed_comp, feed_temp=25):
    duty = 0
    for comp, frac in feed_comp.items():
        mol_flow = frac * feed_flow
        bp = boiling_points[comp]
        hvap = heat_of_vaporization.get(comp, 30000)
        cp = heat_capacity.get(comp, 200)
        sensible_heat = cp * (bp - feed_temp)
        total_heat = (sensible_heat + hvap) * mol_flow
        duty += total_heat
    return duty / 1e6  # GJ/hr

def create_dataframe(products_mol, products_mass, products_bp_sum, products_mol_sum):
    data = []
    for cut in cuts:
        mol = products_mol[cut]
        mass = products_mass[cut]/1000
        if products_mol_sum[cut] > 0:
            avg_bp = products_bp_sum[cut] / products_mol_sum[cut]
        else:
            avg_bp = None
        data.append({
            "Product Cut": cut,
            "Molar Flow (kmol/hr)": mol,
            "Mass Flow (tonnes/hr)": mass,
            "Avg Boiling Point (°C)": avg_bp
        })
    return pd.DataFrame(data)

def plot_distribution(products_mol):
    total_mol = sum(products_mol.values())
    fractions = {cut: mol_flow/total_mol for cut, mol_flow in products_mol.items()}

    fig, ax = plt.subplots()
    bars = ax.bar(fractions.keys(), fractions.values(), color=['skyblue', 'orange', 'green', 'gray'])
    ax.set_ylabel('Molar Fraction')
    ax.set_title('Product Distribution')
    ax.set_ylim(0, 1)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.02, f"{height:.2f}", ha='center')
    return fig

st.title("Crude Distillation Column Simulator")

st.markdown("""
Adjust the feed composition to see the resulting product flows and properties.
""")

# Input sliders
comp_names = ['n-hexane', 'n-octane', 'n-decane', 'benzene', 'toluene']
feed_inputs = {}
total = 0
for comp in comp_names:
    feed_inputs[comp] = st.slider(f"{comp} molar fraction", 0.0, 1.0, float(feed_flow*0.2), 0.01)
    total += feed_inputs[comp]

if total == 0:
    st.warning("Set at least one component fraction > 0.")
else:
    # Normalize
    feed_comp = {comp: val/total for comp, val in feed_inputs.items()}

    products = calculate_products(feed_comp)
    molar_flows, mass_flows, bp_sums, mol_sums, cnum_sums = products

    df = create_dataframe(molar_flows, mass_flows, bp_sums, mol_sums)
    st.subheader("Product Flow Summary")
    st.dataframe(df)

    heat_duty = estimate_heat_duty(feed_comp)
    st.write(f"### Estimated Heat Duty to Vaporize Feed: **{heat_duty:.2f} GJ/hr**")

    fig = plot_distribution(molar_flows)
    st.pyplot(fig)

    # Export button
    towrite = io.BytesIO()
    df.to_csv(towrite, index=False)
    towrite.seek(0)
    st.download_button(
        label="Export Results to CSV",
        data=towrite,
        file_name="distillation_results.csv",
        mime="text/csv"
    )
