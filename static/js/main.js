// Main JavaScript file for the Flask app with Firebase integration

function fetchData() {
    const responseElement = document.getElementById('api-response');
    responseElement.textContent = 'Loading...';
    
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            responseElement.textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            responseElement.textContent = 'Error: ' + error.message;
        });
}

function loadTrades() {
    const tradesElement = document.getElementById('trades-list');
    tradesElement.innerHTML = '<p class="text-muted">Loading trades...</p>';
    
    fetch('/api/trades')
        .then(response => response.json())
        .then(data => {
            if (data.trades && data.trades.length > 0) {
                let tradesHtml = '<div class="table-responsive"><table class="table table-striped"><thead><tr><th>Symbol</th><th>Action</th><th>Quantity</th><th>Price</th><th>Total</th><th>Date</th></tr></thead><tbody>';
                
                data.trades.forEach(trade => {
                    const total = (trade.quantity * trade.price).toFixed(2);
                    const date = new Date(trade.timestamp).toLocaleDateString();
                    const actionClass = trade.action === 'BUY' ? 'text-success' : 'text-danger';
                    
                    tradesHtml += `
                        <tr>
                            <td><strong>${trade.symbol}</strong></td>
                            <td><span class="${actionClass}">${trade.action}</span></td>
                            <td>${trade.quantity}</td>
                            <td>${trade.price}</td>
                            <td>${total}</td>
                            <td>${date}</td>
                        </tr>
                    `;
                });
                
                tradesHtml += '</tbody></table></div>';
                tradesElement.innerHTML = tradesHtml;
            } else {
                tradesElement.innerHTML = '<p class="text-muted">No trades found. Add your first trade!</p>';
            }
        })
        .catch(error => {
            tradesElement.innerHTML = `<p class="text-danger">Error loading trades: ${error.message}</p>`;
        });
}

function loadPortfolioSummary() {
    const summaryElement = document.getElementById('portfolio-summary');
    summaryElement.innerHTML = '<p class="text-muted">Loading portfolio data...</p>';
    
    fetch('/api/trades')
        .then(response => response.json())
        .then(data => {
            if (data.trades && data.trades.length > 0) {
                let totalValue = 0;
                let totalTrades = data.trades.length;
                let symbols = new Set();
                
                data.trades.forEach(trade => {
                    totalValue += trade.quantity * trade.price;
                    symbols.add(trade.symbol);
                });
                
                summaryElement.innerHTML = `
                    <div class="row text-center">
                        <div class="col-4">
                            <h6 class="text-muted">Total Trades</h6>
                            <h4 class="text-primary">${totalTrades}</h4>
                        </div>
                        <div class="col-4">
                            <h6 class="text-muted">Symbols</h6>
                            <h4 class="text-info">${symbols.size}</h4>
                        </div>
                        <div class="col-4">
                            <h6 class="text-muted">Total Value</h6>
                            <h4 class="text-success">${totalValue.toFixed(2)}</h4>
                        </div>
                    </div>
                `;
            } else {
                summaryElement.innerHTML = '<p class="text-muted">No portfolio data available.</p>';
            }
        })
        .catch(error => {
            summaryElement.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
        });
}

function showAddTradeModal() {
    const modal = new bootstrap.Modal(document.getElementById('addTradeModal'));
    modal.show();
}

function addTrade() {
    const form = document.getElementById('addTradeForm');
    const formData = new FormData(form);
    
    const tradeData = {
        symbol: document.getElementById('symbol').value.toUpperCase(),
        action: document.getElementById('action').value,
        quantity: parseInt(document.getElementById('quantity').value),
        price: parseFloat(document.getElementById('price').value)
    };
    
    // Validate form
    if (!tradeData.symbol || !tradeData.action || !tradeData.quantity || !tradeData.price) {
        alert('Please fill in all fields');
        return;
    }
    
    fetch('/api/trades', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(tradeData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('addTradeModal'));
            modal.hide();
            
            // Reset form
            form.reset();
            
            // Refresh data
            loadTrades();
            loadPortfolioSummary();
            
            // Show success message
            showNotification('Trade added successfully!', 'success');
        }
    })
    .catch(error => {
        alert('Error adding trade: ' + error.message);
    });
}

function loadSwingScreener() {
    const screenerElement = document.getElementById('screener-results');
    screenerElement.innerHTML = '<p class="text-muted"><i class="fas fa-spinner fa-spin"></i> Scanning market for swing opportunities...</p>';
    
    fetch('/api/swing-screener')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.stocks && data.stocks.length > 0) {
                let screenerHtml = `
                    <div class="mb-2">
                        <small class="text-muted">Found ${data.count} opportunities • Last scan: ${new Date(data.timestamp).toLocaleTimeString()}</small>
                    </div>
                    <div class="table-responsive" style="max-height: 300px; overflow-y: auto;">
                        <table class="table table-sm table-hover">
                            <thead class="table-light sticky-top">
                                <tr>
                                    <th>Symbol</th>
                                    <th>Price</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                `;
                
                data.stocks.forEach((stock, index) => {
                    screenerHtml += `
                        <tr>
                            <td>
                                <strong>${stock.symbol}</strong>
                                <br><small class="text-muted">${stock.name}</small>
                            </td>
                            <td>₹${stock.close_price}</td>
                            <td>
                                <button class="btn btn-success btn-sm" onclick="addScreenerTrade('${stock.symbol}', ${stock.close_price})">
                                    <i class="fas fa-plus"></i> Add Trade
                                </button>
                            </td>
                        </tr>
                    `;
                });
                
                screenerHtml += '</tbody></table></div>';
                screenerElement.innerHTML = screenerHtml;
            } else {
                screenerElement.innerHTML = '<p class="text-muted">No swing trading opportunities found at the moment.</p>';
            }
        })
        .catch(error => {
            screenerElement.innerHTML = `<p class="text-danger">Error loading screener: ${error.message}</p>`;
        });
}

function addScreenerTrade(symbol, price) {
    // Pre-fill the add trade modal with screener data
    document.getElementById('symbol').value = symbol;
    document.getElementById('price').value = price;
    document.getElementById('action').value = 'BUY'; // Default to BUY for swing trades
    document.getElementById('quantity').value = ''; // Let user enter quantity
    
    // Show the modal
    showAddTradeModal();
    
    // Focus on quantity field
    setTimeout(() => {
        document.getElementById('quantity').focus();
    }, 500);
}
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Add some interactivity
document.addEventListener('DOMContentLoaded', function() {
    console.log('Algorithmic Trading Platform loaded successfully!');
    
    // Load initial data
    loadTrades();
    loadPortfolioSummary();
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});