{% extends "base.html" %}

{% block title %}Home - PowerBI Portal{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h2>Welcome to PowerBI Portal</h2>
    </div>
    <div class="card-body">
        <p>Please select a PowerBI report from the navigation menu.</p>
        
        {% if pages %}
        <div class="row">
            {% for page in pages %}
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ page.title }}</h5>
                        <p class="card-text">{{ page.description }}</p>
                        <a href="{{ url_for('main.view_page', page_id=page.id) }}" class="btn btn-primary">View Report</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="alert alert-info">
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
