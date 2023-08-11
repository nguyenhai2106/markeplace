from django.db.models import Sum
from django.db.models.functions import TruncMinute
from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from menu.models import Category
from orders.models import Order
from vendor.models import Vendor
import pandas as pd
import seaborn as sns
import io

import matplotlib

matplotlib.use('agg')


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


def revenue_report(request):
    orders_by_minute = Order.objects.filter(vendors=get_vendor(request), is_ordered=True).annotate(
        minute=TruncMinute('created_at')).values('minute').annotate(
        total_revenue=Sum('total')).order_by('created_at')

    # Chuyển QuerySet thành DataFrame
    df_revenue = pd.DataFrame(list(orders_by_minute))

    # Tính tổng doanh thu cộng dồn
    df_revenue['cumulative_revenue'] = df_revenue['total_revenue'].cumsum()

    # Vẽ đồ thị doanh thu cộng dồn
    plt.figure(figsize=(10, 6))
    plt.plot(df_revenue['minute'], df_revenue['cumulative_revenue'])
    plt.xlabel('Thời gian')
    plt.ylabel('Doanh Thu ($)')

    # Chuyển đồ thị thành dữ liệu base64
    revenue_buffer = BytesIO()
    plt.savefig(revenue_buffer, format='png')
    revenue_buffer.seek(0)
    revenue_chart_base64 = base64.b64encode(revenue_buffer.read()).decode('utf-8')

    # Truy vấn dữ liệu tổng giá trị đơn hàng
    orders = Order.objects.filter(vendors=get_vendor(request), is_ordered=True)
    df_total = pd.DataFrame(list(orders.values()))

    # Vẽ đồ thị phân phối tổng giá trị đơn hàng
    # Tạo biểu đồ phân phối tổng giá trị đơn hàng bằng Seaborn
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df_total, x='total', bins=20, kde=True)
    plt.xlabel('Giá trị đơn hàng')
    plt.ylabel('Số lượng đơn hàng')

    # Chuyển đồ thị thành dữ liệu base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    distribution_chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    results = Category.objects.filter(vendor=get_vendor(request)).annotate(
        total_amount=Sum('fooditems__orderedfood__amount'))

    result_list = list(results.values('category_name', 'total_amount'))
    df = pd.DataFrame(result_list)
    sizes = df['total_amount']

    # Set up Seaborn style
    sns.set(style="whitegrid")

    def my_autopct(pct):
        value = sizes[int(pct / 100. * len(sizes))]  # Get the actual value from sizes
        return "{:.1f}%\n({:.0f})".format(pct, value)

    # Create a pie chart using Seaborn
    plt.figure(figsize=(10, 6))
    sns.set_palette("pastel")
    plt.pie(df['total_amount'], labels=df['category_name'], autopct=my_autopct, startangle=140)
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close()

    category_ratio_chart_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')  # Rename the variable

    context = {
        'revenue_chart': revenue_chart_base64,
        'distribution_chart': distribution_chart_base64,
        'category_ratio_chart_base64': category_ratio_chart_base64
    }
    return render(request, 'reports/report.html', context)
