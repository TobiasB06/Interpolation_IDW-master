import pandas as pd
import openpyxl as pxl
import numpy as np

class Excel():
    def __init__(self, archive_xlsx,header):
        self.df = pd.read_excel(archive_xlsx, sheet_name="P2-10000", header=header-1)  # Especificamos que el índice de columnas está en la fila 7.

    def create_coordinates_list(self):
        # Encuentra las columnas 'X' y 'Y'.
        x_columns = [col for col in self.df.columns if col.startswith('X')]
        y_columns = [col for col in self.df.columns if col.startswith('Y')]

        coordinates_list = []

        # Itera sobre las filas y crea una lista de coordenadas (X, Y).
        for index, row in self.df.iterrows():
            x_values = [row[x_col] for x_col in x_columns]
            y_values = [row[y_col] for y_col in y_columns]

            # Combina los valores de 'X' y 'Y' en una lista de coordenadas.
            coordinates = list(zip(x_values, y_values))
            coordinates_list.extend(coordinates)

        return coordinates_list

class Interpolation_IDW():
    def __init__(self, archive_xyz, coordinates_list):
        read_data = pd.read_csv(archive_xyz, names=['X', 'Y', 'Z'], delimiter=',')

        interpolated_z_values = []

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
            interpolated_z_values.append(interpolated_z)

        self.interpolated_z_values = interpolated_z_values

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

    def save_to_excel(self, output_excel):
        x_values = [coord[0] for coord in coordinates_list]
        y_values = [coord[1] for coord in coordinates_list]
        z_values = self.interpolated_z_values

        df_result = pd.DataFrame({'X': x_values, 'Y': y_values, 'Z': z_values})
        df_result.to_excel(output_excel, index=False)


if __name__ == '__main__':
    excel = Excel("Archivo_angularesP1.xlsx",7)
    coordinates_list = excel.create_coordinates_list()

    interpolation = Interpolation_IDW("GEBCO-UTN-recorte.xyz", coordinates_list)
    interpolation.save_to_excel("output_result.xlsx")
