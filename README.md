# SACS Joint Load Generator

A free, web-based tool to automate the generation of **SACS Datagen joint load input lines** directly from Excel files.

✅ Built for offshore structural engineers.  
✅ Created by [Sajjad Babamohammadi](https://www.linkedin.com/in/sajjad-b-7aab1b172/)  
✅ Use it instantly here: [🌐 Launch Web App](https://sacs-joint-load-generator.onrender.com/) 

---

## 🔧 What It Does

This tool converts cleaned-up Excel load data into correctly formatted `.txt` output lines that match the **SACS Datagen format**, including:

- Load Condition blocks  
- Joint-level forces and moments (Fx, Fy, Fz, Mx, My, Mz)  
- Automatic character alignment  
- Rounding with log of modified values  
- Clean, ready-to-copy output

---

## 📥 Input Format

The Excel file must contain a header row with the following columns:

| Column         | Description                      |
|----------------|----------------------------------|
| Load Condition | (e.g. S100, S200…)               |
| Load ID        | A name for the load (max 8 chars)|
| Joint Name     | Joint name (exactly 4 chars)     |
| FORCE(X)       | X-direction force                |
| FORCE(Y)       | Y-direction force                |
| FORCE(Z)       | Z-direction force                |
| MOMENT(X)      | X-moment                         |
| MOMENT(Y)      | Y-moment                         |
| MOMENT(Z)      | Z-moment                         |

Each load condition can include multiple load IDs. Leave the "Load Condition" cell empty to continue the block.

---

## 📤 Output Example
LOADCNLS11
LOAD LS11 2507 5537 -93643 123.0 0.0 11032 GLOB JOIN LS11


- Each line is exactly **datagen format**
- Fields are **right-aligned and fixed-width**
- Overlong values are safely rounded

---

## 👨‍💻 Technology Stack

- Python 3
- [Streamlit](https://streamlit.io) for UI
- Deployed on [Render.com](https://render.com)

---

## 📢 Share & Support

This tool was built to save time and reduce manual errors during SACS input preparation.  
If it helps you, please ⭐ star the repo or share it with your team!

---

## 🧑‍🎓 Author

**Sajjad Babamohammadi**  
Offshore Structural Engineer | SACS | FEM | Python  
[LinkedIn →](https://www.linkedin.com/in/sajjad-b-7aab1b172/)


