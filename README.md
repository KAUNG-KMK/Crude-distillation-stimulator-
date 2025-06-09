# Crude Distillation Column Simulator

An interactive web application simulating a simplified petroleum refinery crude distillation column built with Python and Streamlit.

---

## Project Overview

This project models the atmospheric distillation of crude oil into major product cuts such as Naphtha, Kerosene, Diesel, and Residue. Users can adjust the molar composition of typical crude components and instantly see the resulting product flow rates, average boiling points, and estimated heat duty required for vaporization.

The application aims to provide a hands-on tool for chemical engineering students and professionals to understand the basics of refinery distillation through an accessible and interactive interface.

---

## Features

- **Interactive Feed Composition:** Adjust molar fractions of key hydrocarbons (n-hexane, n-octane, n-decane, benzene, toluene) via sliders.
- **Product Flow Calculation:** Calculates molar and mass flow rates for refinery product cuts.
- **Average Property Estimation:** Determines average boiling points for each product cut.
- **Heat Duty Estimation:** Estimates total energy required to vaporize the feed stream.
- **Visual Product Distribution:** Bar chart visualization of product molar fractions.
- **CSV Export:** Download simulation results for offline analysis or reporting.

---

## Installation & Running

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/crude-distillation-simulator.git
    cd crude-distillation-simulator
    ```

2. Install dependencies:

    ```bash
    pip install streamlit pandas matplotlib
    ```

3. Run the app:

    ```bash
    streamlit run app.py
    ```

4. The app will open in your default web browser.

---

## Usage

- Use the sliders to set molar fractions of each component in the crude feed.
- View updated product flow tables, heat duty, and product distribution chart.
- Click the **Export Results to CSV** button to download simulation data.

---

## Future Enhancements

- Incorporate vapor-liquid equilibrium (VLE) calculations for more accurate separation modeling.
- Add temperature and pressure profile simulation inside the distillation column.
- Expand component list and refine physical property databases.
- Deploy as a public web app for wider accessibility.

---

## License

This project is licensed under the MIT License.

---

## Contact

Created by [Your Name] — Chemical Engineering Student  
[GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile)
