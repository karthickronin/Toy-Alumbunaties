# GitHub Pages Deployment Guide

## 🚀 How to Deploy Your Toy Alumbunaties Website to GitHub Pages

### Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon and select "New repository"
3. Name your repository (e.g., `toy-alumbunaties-website`)
4. Make sure it's set to **Public**
5. Click "Create repository"

### Step 2: Upload Your Files

1. In your new repository, click "uploading an existing file"
2. Drag and drop all files from the `docs` folder to GitHub
3. Or use Git commands:

```bash
git init
git add .
git commit -m "Initial website deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. Scroll down to **Pages** section (left sidebar)
4. Under "Source", select **Deploy from a branch**
5. Choose **main** branch
6. Choose **/ (root)** folder (since our files are in the root)
7. Click **Save**

### Step 4: Access Your Website

After a few minutes, your website will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPOSITORY_NAME/
```

## 📁 File Structure

Your `docs` folder contains:
```
docs/
├── index.html          # Home page
├── about.html          # About page
├── services.html       # Services page
├── gallery.html        # Gallery page
├── contact.html        # Contact page
├── style.css          # Main stylesheet
├── static/            # Images, videos, assets
├── _config.yml        # GitHub Pages configuration
└── README.md          # Documentation
```

## 🎨 Customization

### Update Content
- Edit the HTML files to change text, images, or layout
- Modify `style.css` to change colors, fonts, or styling
- Replace images in the `static` folder with your own

### Update Contact Information
- Update phone numbers in all HTML files
- Change social media links in the footer
- Modify the contact form WhatsApp integration

### Add More Images/Videos
1. Upload new files to the `static` folder
2. Update the gallery.html file to include new media
3. Commit and push changes to GitHub

## 🔧 Advanced Features

### Custom Domain (Optional)
1. Buy a domain name (e.g., toyalumbunaties.com)
2. In your repository settings > Pages
3. Add your custom domain
4. Configure DNS settings with your domain provider

### Analytics (Optional)
Add Google Analytics by inserting the tracking code in all HTML files before the closing `</head>` tag.

### SEO Optimization
- Update meta descriptions in each HTML file
- Add relevant keywords
- Optimize image alt texts
- Create a sitemap.xml file

## 📱 Mobile Responsiveness

The website is already mobile-responsive using Bootstrap 5, but you can test and improve:
- Test on different screen sizes
- Optimize images for mobile
- Ensure touch-friendly buttons

## 🚨 Troubleshooting

### Website Not Loading?
- Check if GitHub Pages is enabled in repository settings
- Ensure files are in the correct location
- Wait 5-10 minutes for changes to propagate

### Images Not Showing?
- Check file paths in HTML files
- Ensure images are uploaded to the `static` folder
- Verify image file names match exactly (case-sensitive)

### Contact Form Not Working?
- The form currently redirects to WhatsApp
- For email forms, you'll need a backend service like Formspree or Netlify Forms

## 📞 Support

If you need help with deployment or customization:
- **Deepak**: 9360895326
- **Jeeva**: 9342569205
- **Jeeva**: 8122626281

## 🎉 Success!

Once deployed, your website will be live and accessible to anyone with the URL. Share it with your customers and start booking more events!

---

**Happy Hosting! 🎭**