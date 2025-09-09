import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def discover_formula(x_data, y_data, z_data, degree=3):
    """Discover formula for z = f(x,y) using polynomial regression"""
    # Prepare data
    X = np.array([[x, y] for x, y, z in zip(x_data, y_data, z_data)])
    Z = np.array(z_data)
    
    # Create polynomial features
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    
    # Fit the model
    model = LinearRegression()
    model.fit(X_poly, Z)
    
    # Evaluate the model
    Z_pred = model.predict(X_poly)
    r2 = r2_score(Z, Z_pred)
    
    # Get the formula
    feature_names = poly.get_feature_names_out(['x', 'y'])
    formula = f"z = {model.intercept_:.4f}"
    for coef, name in zip(model.coef_, feature_names):
        if coef != 0:
            formula += f" + {coef:.4f}*{name}"
    
    return {
        'formula': formula,
        'coefficients': model.coef_,
        'intercept': model.intercept_,
        'r2_score': r2,
        'model': model,
        'poly': poly
    }
    
    
def discover_fourier_formula(x_data, y_data, z_data, max_terms=3):
    """Discover formula using Fourier components for periodic functions"""
    X = np.array([[x, y] for x, y, z in zip(x_data, y_data, z_data)])
    Z = np.array(z_data)
    
    # Create Fourier features
    features = []
    feature_names = []
    
    for i in range(len(X)):
        row = [1.0]  # Constant term
        names = ['1']
        
        x, y = X[i]
        # Add sine and cosine terms
        for n in range(1, max_terms + 1):
            row.extend([
                np.sin(n * x), np.cos(n * x),
                np.sin(n * y), np.cos(n * y)
            ])
            names.extend([
                f'sin({n}x)', f'cos({n}x)',
                f'sin({n}y)', f'cos({n}y)'
            ])
        
        features.append(row)
    
    X_fourier = np.array(features)
    
    # Fit model
    model = LinearRegression()
    model.fit(X_fourier, Z)
    
    # Create formula
    formula = f"z = {model.intercept_:.4f}"
    for coef, name in zip(model.coef_, names):
        if abs(coef) > 0.001:  # Only include significant terms
            formula += f" + {coef:.4f}*{name}"
    
    return {
        'formula': formula,
        'coefficients': model.coef_,
        'intercept': model.intercept_,
        'model': model
    }
    
def polynomial_regression(x_data, y_data, z_data, degree=3):
    """Fit a polynomial regression model to your 2D data"""
    import numpy as np
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    
    # Prepare input data
    X = np.array([[x, y] for x, y in zip(x_data, y_data)])
    y = np.array(z_data)
    
    # Create polynomial features
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    
    # Fit the model
    model = LinearRegression()
    model.fit(X_poly, y)
    
    # Evaluate the model
    y_pred = model.predict(X_poly)
    r2 = r2_score(y, y_pred)
    
    # Create prediction function
    def predict_z(x_new, y_new):
        X_new = np.array([[x_new, y_new]])
        X_new_poly = poly.transform(X_new)
        return model.predict(X_new_poly)[0]
    
    # Print formula
    feature_names = poly.get_feature_names_out(['x', 'y'])
    formula = f"z = {model.intercept_:.4f}"
    for coef, name in zip(model.coef_, feature_names):
        if abs(coef) > 0.001:  # Only include significant terms
            formula += f" + {coef:.4f}*{name}"
    
    return {
        'model': model,
        'predict': predict_z,
        'r2_score': r2,
        'formula': formula,
        'coefficients': model.coef_,
        'intercept': model.intercept_
    }






    
    
#     # Extract data points
# x_data = []
# y_data = []
# z_data = []
# for x_key in z:
#     for y_key in z[x_key]:
#         x_data.append(x_key)
#         y_data.append(y_key)
#         z_data.append(z[x_key][y_key])

# # Fit polynomial model
# model_info = polynomial_regression(x_data, y_data, z_data, degree=2)

# # Print results
# print(f"Polynomial formula: {model_info['formula']}")
# print(f"R² score: {model_info['r2_score']:.4f}")

# # Create surface using the model
# plot_manager.figure(figsize=(12, 6))
# plot_manager.plot_surface(x_range, y_range, model_info['predict'], linewidth=0)
# plot_manager.title('Equation of Time Model using Polynomial Regression')
# plot_manager.show('Equation_of_Time_Polynomial_Model.png')