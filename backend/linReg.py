import json
from sklearn.linear_model import LinearRegression
import numpy as np

def linReg(request):
    """Receives JSON data, performs linear regression, and returns the results."""
    # Get the request body
    data = request.get_json()

    # Extract the input data from the JSON
    X = np.array(data['X'])
    y = np.array(data['y'])

    # Perform linear regression
    model = LinearRegression()
    model.fit(X.reshape(-1, 1), y)

    # Get the regression coefficients
    slope = model.coef_[0]
    intercept = model.intercept_

    # Prepare the response
    response = {
        'slope': slope,
        'intercept': intercept
    }

    # Return the response as JSON
    return json.dumps(response)