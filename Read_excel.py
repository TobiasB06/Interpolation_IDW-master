import pandas as pd
import openpyxl as pxl
import numpy as np

import pandas as pd

class Excel():
    def __init__(self,archive_xlsx,header,sheet):
        self.df = pd.read_excel(archive_xlsx, sheet_name=sheet, header=header-1) 

    def create_coordinates_list(self):
        # Encuentra las columnas 'X' y 'Y'.
        x_columns = [col for col in self.df.columns if col.startswith('X')]
        y_columns = [col for col in self.df.columns if col.startswith('Y')]

        coordinates_list = []
        for index, row in self.df.iterrows():
            x_values = [row[x_col] for x_col in x_columns]
            y_values = [row[y_col] for y_col in y_columns]

            # Combina los valores de 'X' y 'Y' en una lista de coordenadas.
            coordinates = list(zip(x_values, y_values))
            coordinates_list.extend(coordinates)
        print(coordinates_list)
        return coordinates_list

class Interpolation_IDW():
    def __init__(self, df, archive_xyz, coordinates_list):
        self.df = df  # Asigna el DataFrame desde Excel
        read_data = pd.read_csv(archive_xyz, names=['X', 'Y', 'Z'], delimiter=',')
        self.coordinates_list = coordinates_list

        self.interpolated_z_values = []

        for x_interest, y_interest in coordinates_list:
            # Closest points 
            read_data['distancia'] = np.sqrt((read_data['X'] - x_interest)**2 + (read_data['Y'] - y_interest)**2)
            closest_points = read_data.nsmallest(6, 'distancia')

            # Main Coefficient for IDW
            p = 2.0
            # Closest X, Y y Z points
            x = closest_points['X'].values
            y = closest_points['Y'].values
            z = closest_points['Z'].values
        
            interpolated_z = self.interpolation_idw(x, y, z, x_interest, y_interest, p)
            self.interpolated_z_values.append(interpolated_z)

    # Interpolation IDW(Inverse Distance Weighting)
    def interpolation_idw(self, x, y, z, x_interest, y_interest, p):
        weights = 0
        z_weights = 0
        for i in range(len(x)):
            distance = np.sqrt((x_interest - x[i])**2 + (y_interest - y[i])**2)
            weight = 1 / (distance**p)
            weights += weight
            z_weights += weight * z[i]
        return z_weights / weights

    def save_to_excel(self, num_rows_per_file=106):
        for i in range(0, len(self.coordinates_list), num_rows_per_file):
            subset_coordinates = self.coordinates_list[i:i + num_rows_per_file]
            subset_z_values = self.interpolated_z_values[i:i + num_rows_per_file]

            df_result = pd.DataFrame({'X': [coord[0] for coord in subset_coordinates],
                                    'Y': [coord[1] for coord in subset_coordinates],
                                    'Z': subset_z_values})

            output_excel = f"Punto_{i//num_rows_per_file}.xlsx"
            df_result.to_excel(output_excel, index=False)

if __name__ == '__main__':
    excel = Excel("Prueba1.xlsx", 7,"Hoja1")
    coordinates_list = excel.create_coordinates_list()
    interpolation = Interpolation_IDW(excel.df, "GEBCO-UTN-recorte.xyz", coordinates_list)
    interpolation.save_to_excel()

