function nlp
problem = struct( ...
    'f_fcn',    @(x)f2(x), ...
    'gh_fcn',   @(x)gh2(x), ...
    'hess_fcn', @(x, lam)hess2(x, lam), ...
    'x0',       [1; 1; 0], ...
    'opt',      struct('verbose', 2) ...
);

[x, f, exitflag, output, lambda] = mips(problem);

f

function [f, df, d2f] = f2(x)
f = -x(1)*x(2) - x(2)*x(3);
if nargout > 1           %% gradient is required
    df = -[x(2); x(1)+x(3); x(2)];
    if nargout > 2       %% Hessian is required
        d2f = -[0 1 0; 1 0 1; 0 1 0];   %% actually not used since
    end                                 %% 'hess_fcn' is provided
end

function [h, g, dh, dg] = gh2(x)
h = [ 1 -1 1; 1 1 1] * x.^2 + [-2; -10];
dh = 2 * [x(1) x(1); -x(2) x(2); x(3) x(3)];
g = []; dg = [];

function Lxx = hess2(x, lam)
mu = lam.ineqnonlin;
Lxx = [2*[1 1]*mu -1 0; -1 2*[-1 1]*mu -1; 0 -1 2*[1 1]*mu];
