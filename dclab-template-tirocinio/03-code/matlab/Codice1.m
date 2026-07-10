% Esempio: calcolo iterativo del gradiente proiettato
function x = projected_gradient(grad, project, x0, step, tol, max_iter)
if nargin < 4, step = 0.01; end
if nargin < 5, tol = 1e-6; end
if nargin < 6, max_iter = 1000; end

x = x0;
for k = 1:max_iter
    x_new = project(x - step * grad(x));
    if norm(x_new - x) < tol
        x = x_new;
        return
    end
    x = x_new;
end
end
